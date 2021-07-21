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
* Strictest tests (Travis CI takes a long time) and require at least 1 code review
* Only certain people in the org can merge changes
* Make sure you run `make sanity` before a PR 
* If your change warrants documentation changes, check if you need to run `make` to automatically generate any other docs

#### Try a Pull Request
1. Make sure you have a github account set up. Optionally, set up a git client on your machine as well (I use the CLI from my Mac terminal) and set up any credentials you might need.
2. Fork the [go-algorand](https://github.com/algorand/go-algorand) repo using your github credential. Make a new branch (`git checkout -b name-of-your-branch`) and start developing on there.
3. On your editor (I use VS Code or vim), make a small change like adding a unit test. Save and try commiting your changes.
4. Make more changes if desired. Commit, and repeat. If new commits have popped up in the main repo, make sure you `git pull` the latest changes from the remote. 
5. Run `make sanity` before you submit your PR, or else your code may not pass the Travis CI style checks (and waste 30min of your time). 
6. When you are ready, push the changes (squashing is optional), and open up a Pull Request on the Github client. 
7. It is generally prudent to double check the diffs and make sure you are okay with your own changes. Try to confirm that your code passes all the Travis CI checks.
8. Request some reviewers for feedback.
9. After feedback is addressed and the changes are approved, they can be merged by an authorized member. After it has been merged, feel free to delete the branch you were working on. 
