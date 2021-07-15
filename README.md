# Algorand Onboarding

A collection of notes and potentially useful stuff as I onboard.

## Contents
  * [Basics](#basics)
    + [Installing a node](#installing-a-node)
    + [Switching networks](#switching-networks)
  * [TEAL Contracts](#teal-contracts)
    + [Stateful Contracts](#stateful-contracts)
  * [Development](#development)



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

#### My node isn't catching up!
Double check that your node is up to date. If there has been a protocol change, you will not be able to sync current blocks on an older node. 

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

### PyTeal
[Pyteal](https://github.com/algorand/pyteal) can generate TEAL code by using Python code. 

Here is an example game that uses PyTeal to generate a smart contract to play Battleship: [AlgoShip](https://github.com/jasonpaulos/algoship)

You can also examine transactions on the Algorand blockchain (Mainnet, Testnet, etc.) using [Algoexplorer](https://testnet.algoexplorer.io/). Try searching up your sample transaction by sender address and more!

## Development
### [go-algorand](https://github.com/algorand/go-algorand)
* When you are making changes, fork the repo and create a branch for the change in your local fork
* Strictest tests (Travis CI takes a long time)
* Only certain people in the org can merge changes
* Make sure you run `make sanity` before a PR 
* If your change warrants documentation changes, check if you need to run `make` to automatically generate any other docs

