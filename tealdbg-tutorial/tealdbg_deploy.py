import base64
import os
from pathlib import Path
import pty
import random
import subprocess

from algosdk import account, encoding, mnemonic, logic
from algosdk.future import transaction
from algosdk.v2client import algod, indexer


sandbox_exec = Path(os.environ["SANDBOX_PATH"]) / "sandbox"
output_path = Path(os.path.dirname(os.path.realpath(__file__))) / "generated-data"


def create_algod_client():
    return algod.AlgodClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "http://localhost:4001",
    )


def create_indexer_client():
    return indexer.IndexerClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "http://localhost:8980",
    )


def compile_program(client, source_code):
    compile_response = client.compile(source_code.decode("utf-8"))
    return base64.b64decode(compile_response["result"])


def get_sandbox_account():
    stdout = subprocess.run(
        [sandbox_exec, "goal", "account", "list"],
        stdin=pty.openpty()[1],
        capture_output=True,
        text=True,
    ).stdout
    return stdout.split()[1]


def export_sandbox_account():
    genesis_addr = get_sandbox_account()
    stdout = subprocess.run(
        [sandbox_exec, "goal", "account", "export", "-a", genesis_addr],
        stdin=pty.openpty()[1],
        capture_output=True,
        text=True,
    ).stdout
    passwd_string = stdout.split()[5:]
    passwd_string = " ".join(passwd_string)
    passwd = passwd_string.replace('"', "")
    return passwd


def get_funded_account():
    passphrase = export_sandbox_account()
    pk = mnemonic.to_private_key(passphrase)
    addr = account.address_from_private_key(pk)
    return pk, addr


def create_transient_account(client, sender, private_key):
    sk, pk = account.generate_account()
    txn = transaction.PaymentTxn(
        sender,
        client.suggested_params(),
        pk,
        random.randrange(10, 100) * 3000000,
    )
    stxn = txn.sign(private_key)
    tx_id = stxn.transaction.get_txid()
    client.send_transaction(stxn)
    transaction.wait_for_confirmation(client, tx_id, 5)
    return sk, pk


# Uses sandbox to call goal clerk dryrun
def create_debugger_context(output_path, context_file, output_file):
    sandbox_copyto = f"{sandbox_exec} copyTo {context_file}"
    dry_run_command = f"{sandbox_exec} goal clerk dryrun -t {context_file} --dryrun-dump -o {output_file}"
    sandbox_copyfrom = f"{sandbox_exec} copyFrom {output_file}"

    # Change CWD to structure copy commands in a sanbox container compliant manner.
    cwd = os.getcwd()
    os.chdir(output_path)

    os.system(sandbox_copyto)
    os.system(dry_run_command)
    os.system(sandbox_copyfrom)
    os.chdir(cwd)


# Uses the native Python SDK function to create dryrun dump
def create_dryrun_dump(stxns, output_path, output_file):
    if not isinstance(stxns, list):
        stxns = [stxns]
    drr = transaction.create_dryrun(client, stxns)

    filename = output_path / output_file
    with open(filename, "wb") as f:
        f.write(base64.b64decode(encoding.msgpack_encode(drr)))


# Create global account and clients
client = create_algod_client()
private_key, sender = get_funded_account()
params = client.suggested_params()

# Creates a stateful app for testing
# The TEAL code for the app can be changed in sample-teal/
def create_test_app(output_path):

    # Create transient
    sk, pk = create_transient_account(client, sender, private_key)

    # Declare application state storage (immutable)
    local_ints = 1
    local_bytes = 1
    global_ints = 1
    global_bytes = 1

    # Define app schema
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)
    on_complete = transaction.OnComplete.NoOpOC.real

    # Compile the program with algod
    source_code = ""
    clear_code = ""
    with open("some_itxns.teal", mode="rb") as file:
        source_code = file.read()
    with open("clear.teal", mode="rb") as file:
        clear_code = file.read()
    source_program = compile_program(client, source_code)
    clear_program = compile_program(client, clear_code)

    # Create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        pk,
        params,
        on_complete,
        source_program,
        clear_program,
        global_schema,
        local_schema,
    )

    # Sign transaction with funded private key
    signed_txn = txn.sign(sk)
    tx_id = signed_txn.transaction.get_txid()

    # Write stxn to file
    transaction.write_to_file([signed_txn], output_path / "signed_txn_create.txn")

    # Send transaction
    client.send_transactions([signed_txn])

    # Wait for response
    print("Waiting for blocks...")
    resp = transaction.wait_for_confirmation(client, tx_id, 5)
    print(f"Response: {resp}")

    app_id = resp["application-index"]
    return app_id


def call_app(app_id, output_path, output_file):
    txn1 = transaction.PaymentTxn(
        sender,
        params,
        logic.get_application_address(app_id),
        random.randrange(10, 100) * 700000,
    )
    txn2 = transaction.ApplicationNoOpTxn(
        sender=sender,
        sp=params,
        index=app_id,
    )

    # Group the txns
    stxns = []
    txn_group = [txn1, txn2]
    gid = transaction.calculate_group_id(txn_group)
    for t in txn_group:
        t.group = gid
        stxn = t.sign(private_key)
        stxns.append(stxn)

    tx_id = stxns[0].get_txid()

    # Write stxn to file
    transaction.write_to_file(stxns, output_path / output_file)

    # # Send transaction (optional for debugging)
    # client.send_transactions(stxns)
    # resp = transaction.wait_for_confirmation(client, tx_id, 5)
    # print(f"Response: {resp}")

    return stxns


output_path.mkdir(exist_ok=True)

app_id = create_test_app(output_path)
stxns = call_app(
    app_id=app_id,
    output_path=output_path,
    output_file="signed_txn.txn",
)
# Use the Python SDK to create dryrun dump
create_dryrun_dump(
    stxns=stxns,
    output_path=output_path,
    output_file="dryrun_txn.msgp",
)

# Uses sandbox goal to create dryrun dump
# create_debugger_context(
#     output_path=output_path,
#     context_file="signed_txn.txn",
#     output_file="dryrun_txn.msgp",
# )
