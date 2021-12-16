import base64

from algosdk.v2client import algod, indexer

# Use this if you already have sandbox running.
# You can also replace the endpoint with your own or a publicly available one.
def create_algod_client():
    return algod.AlgodClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "http://localhost:4001",
    )


def compile_program(client, source_code):
    compile_response = client.compile(source_code.decode("utf-8"))
    return base64.b64decode(compile_response["result"])


# Compile the program with algod
source_code = ""
with open("teal/simple.teal", mode="rb") as file:
    source_code = file.read()

client = create_algod_client()
source_program = compile_program(client, source_code)
print(source_program)
