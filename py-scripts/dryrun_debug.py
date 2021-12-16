import base64
import json
import subprocess
import pty
import random
import time
from algosdk import account, mnemonic
from algosdk.v2client.models import DryrunRequest, DryrunSource
from algosdk.future.transaction import (
    wait_for_confirmation,
    PaymentTxn,
    LogicSig,
    LogicSigTransaction,
)
from algosdk.v2client import algod

# Add your custom path to sandbox here
SANDBOX_PATH = "../../sandbox/sandbox"

# Note: These are sandbox endpoints and tokens.
def create_algod_client():
    return algod.AlgodClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "http://localhost:4001",
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
private_key, sender = get_funded_account()
params = client.suggested_params()


def dryrun_debug(lstx, mysource):
    sources = []
    if mysource != None:
        # source
        sources = [DryrunSource(field_name="lsig", source=mysource, txn_index=0)]
    drr = DryrunRequest(txns=[lstx], sources=sources)
    dryrun_response = client.dryrun(drr)
    return dryrun_response


def dryrun_lsig():
    # Compile the program with algod
    source_code = ""
    with open("dryrun_example.teal", mode="rb") as file:
        source_code = file.read()
    source_program = compile_program(client, source_code)

    arg1 = (123).to_bytes(8, "big")
    lsig = LogicSig(source_program, args=[arg1])

    lsig.sign(private_key=private_key)

    txn = PaymentTxn(sender, params, sender, 100000 + random.randint(1, 1000), None)
    # Create the LogicSigTransaction with contract account LogicSig
    lstx = LogicSigTransaction(txn, lsig)

    dryrun_response_compiled = dryrun_debug(lstx, None)
    # print ("COMPILED Dryrun results...")
    print(json.dumps(dryrun_response_compiled, indent=2))

    # source
    # dryrun_respone_source = dryrun_debug(lstx, source)
    # print("SOURCE Dryrun results...")
    # print(json.dumps(dryrun_respone_source, indent=2))

    txid = client.send_transaction(lstx)
    print("Transaction ID: " + txid)
    wait_for_confirmation(client, txid, 10)


dryrun_lsig()
