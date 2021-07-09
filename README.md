# Algorand Playground

A collection of notes and potentially useful stuff as I onboard.

## Contents
  * [Basics](#basics)
    + [Installing a node](#installing-a-node)
    + [Switching networks](#switiching-networks)
  * [TEAL Contracts](#teal-contracts)
    + [Stateful Contracts](#stateful-contracts)



## Basics
### Installing a node
[Installing on a Mac](https://developer.algorand.org/docs/run-a-node/setup/install/#installing-on-a-mac)

### Switching Networks
If you followed the instructions above, the Algorand node will probably run on the Mainnet. You probably want to use the Testnet though, as it won't cost actual Algos to operate on the Testnet, contrary to the Mainnet. Basically, start the chain with the Testnet genesis block and sync to network [Instructions here](https://developer.algorand.org/docs/run-a-node/operations/switch_networks/).

```
cd ~/node
./goal node stop -d [data]
mkdir testnetdata 
cp ~/node/genesisfiles/testnet/genesis.json ~/node/testnetdata
```

### Catchup
You can check the status of your node in testnet with:

`goal node status -d ~/node/testnetdata`

[Using fast catchup using known checkpoints](https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup):

`./goal node catchup [1234#YOURCHECKPOINTHERE] -d ~/node/testnetdata`

Latest Testnet checkpoint: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint

### Making an account
Start kmd on a private network or testnet node:

`$ ./goal kmd start -d [data directory]`

Next, create a wallet and an account:

`$ ./goal wallet new [wallet name] -d [data directory]`

`$ ./goal account new -d [data directory] -w [wallet name]`

### Funding accounts
On the testnet, there is a bank that gives out free Algos: [Bank](https://bank.testnet.algorand.network/)


## TEAL Contracts
[Compiling contracts using goal clerk](https://medium.com/algorand/understanding-algorand-smart-contracts-b9fc743e7a0f)

You can compile contracts using `goal clerk`

`goal clerk compile simple.teal -d ~/node/testnetdata`

You can also disassemble them and inspect it closer:
```
goal clerk compile subby.teal -d ~/node/testnetdata -o mysubbybin.tealc
goal clerk compile  -d ~/node/testnetdata -D mybin.tealc
```

### Stateful Contracts
[Tutorial here](https://developer.algorand.org/docs/features/asc1/stateful/hello_world)