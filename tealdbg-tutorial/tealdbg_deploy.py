import base64
import os
from random import randrange
import subprocess
import pty
import time

from algosdk import account, mnemonic, logic
from algosdk.future import transaction
from algosdk.v2client import algod, indexer


SANDBOX_PATH = ""  # Your sandbox path here
SLEEP_TIME = 6  # seconds


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
        [SANDBOX_PATH, "goal", "account", "list"],
        stdin=pty.openpty()[1],
        capture_output=True,
        text=True,
    ).stdout
    return stdout.split()[1]


def export_sandbox_account():
    genesis_addr = get_sandbox_account()
    stdout = subprocess.run(
        [SANDBOX_PATH, "goal", "account", "export", "-a", genesis_addr],
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


# Create global account and clients
client = create_algod_client()
ind_client = create_indexer_client()
private_key, sender = get_funded_account()
params = client.suggested_params()


def create_transient_account(sender, private_key):
    sk, pk = account.generate_account()
    txn = transaction.PaymentTxn(
        sender,
        params,
        pk,
        randrange(10, 100) * 3000000,
    )
    stxn = txn.sign(private_key)
    client.send_transaction((stxn))
    time.sleep(SLEEP_TIME)
    return sk, pk


# Creates a stateful app for testing
# The TEAL code for the app can be changed in sample-teal/
def create_test_app():
    # Create transient
    sk, pk = create_transient_account(sender, private_key)

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
    with open("some_logs.teal", mode="rb") as file:
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction.write_to_file([signed_txn], dir_path + "/logs_signed.txn")

    # Send transaction
    client.send_transactions([signed_txn])

    # Wait for response
    print("Waiting for blocks...")
    resp = transaction.wait_for_confirmation(client, tx_id, 5)
    print(f"Response: {resp}")

    app_id = resp["application-index"]
    return app_id


def call_app(app_id):
    txn1 = transaction.PaymentTxn(
        sender,
        params,
        logic.get_application_address(app_id),
        randrange(10, 100) * 700000,
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction.write_to_file(stxns, dir_path + "/logs_signed.txn")

    # Send transaction
    client.send_transactions(stxns)
    resp = transaction.wait_for_confirmation(client, tx_id, 5)
    print(f"Response: {resp}")


app_id = create_test_app()
call_app(app_id)
