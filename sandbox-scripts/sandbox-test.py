"""
The following script should only be used for TESTING PURPOSES (on sandbox).
DO NOT expose your secrets to the outside world.
"""

import base64
import subprocess
import pty
import time
from algosdk import account, mnemonic
from algosdk.future import transaction
from algosdk.v2client import algod, indexer

# Add your custom path to sandbox here
SANDBOX_PATH = "../../sandbox/sandbox"

# Note: These are sandbox endpoints and tokens.
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
    sk = mnemonic.to_private_key(passphrase)
    addr = account.address_from_private_key(sk)
    return sk, addr


def get_transient_account(client):
    funded_sk, funded_pk = get_funded_account()
    sk, pk = account.generate_account()
    txn = transaction.PaymentTxn(
        funded_pk,
        client.suggested_params(),
        pk,
        3000000,
    )
    stxn = txn.sign(funded_sk)
    tx_id = client.send_transaction((stxn))
    transaction.wait_for_confirmation(client, tx_id, 5)
    return sk, pk


# Creates a stateful app for testing
# The TEAL code for the app can be changed in sample-teal/
def create_test_app():
    # Declare application state storage (immutable)
    local_ints = 1
    local_bytes = 1
    global_ints = 1
    global_bytes = 0

    # Define app schema
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)
    on_complete = transaction.OnComplete.NoOpOC.real

    client = create_algod_client()
    ind_client = create_indexer_client()

    # Compile the program with algod
    source_code = ""
    clear_code = ""
    with open("sample-teal/simple.teal", mode="rb") as file:
        source_code = file.read()
    with open("sample-teal/clear.teal", mode="rb") as file:
        clear_code = file.read()
    source_program = compile_program(client, source_code)
    clear_program = compile_program(client, clear_code)

    # Prepare the transaction
    params = client.suggested_params()

    # Note: Currently accounts have a 10 app limit, so create a transient
    # account if you wish to run this script many times.
    private_key, sender = get_funded_account() # get_transient_account(client)

    # Create an unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        source_program,
        clear_program,
        global_schema,
        local_schema,
    )

    # Sign transaction with funded private key
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Display results (may take ~20 seconds)
    # On a "real" network, we need to add artificial delays so the blocks
    # can be finalized.
    # On a "dev" network, we do not need to sleep the program as much as blocks
    # are (almost) instantly finalized.
    print("Waiting for blocks...")

    transaction_response = transaction.wait_for_confirmation(client, tx_id, 5)
    print(transaction_response)
    app_id = transaction_response["application-index"]
    algod_response = client.application_info(app_id)
    print(algod_response)

    # If you are on dev mode, then you may need to send another transaction for
    # Indexer to sync properly.
    time.sleep(10)
    indexer_response = ind_client.applications(app_id)
    print(indexer_response)


create_test_app()
