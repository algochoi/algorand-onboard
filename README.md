# Algorand Onboarding

A collection of notes and potentially useful stuff as I onboard.

- [Algorand Onboarding](#algorand-onboarding)
  * [Contents](#contents)
  * [Basics](#basics)
    + [Installing a node](#installing-a-node)
    + [Switching Networks](#switching-networks)
    + [Sandbox](#sandbox)
  * [TEAL Contracts](#teal-contracts)
    + [Stateless Contracts](#stateless-contracts)
    + [Stateful Contracts](#stateful-contracts)
    + [PyTeal](#pyteal)
  * [Development](#development)
  * [Testing](#testing)
    + [go-algorand](#go-algorand)
    + [SDKs](#sdks)
  * [Indexer](#indexer)

## Basics
### Installing a node
[Installing on a Mac](https://developer.algorand.org/docs/run-a-node/setup/install/#installing-on-a-mac)

### Switching Networks
If you followed the instructions above, the Algorand node will probably run on the MainNet. You probably want to use the TestNet though, as it won't cost actual Algos to operate on the TestNet, contrary to the MainNet. Basically, start the chain with the TestNet genesis block and sync to network [Instructions here](https://developer.algorand.org/docs/run-a-node/operations/switch_networks/).

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

Latest TestNet checkpoint: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint

#### My node isn't catching up!
Double check that your node is up to date. If there has been a protocol change, you will not be able to sync current blocks on an older node. 

### Making an account
Start kmd on a private network or testnet node:

`$ ./goal kmd start -d [data directory]`

Next, create a wallet and an account:

`$ ./goal wallet new [wallet name] -d [data directory]`

`$ ./goal account new -d [data directory] -w [wallet name]`

### Funding accounts
On the TestNet, there is a bank that gives out free Algos: [Bank](https://bank.testnet.algorand.network/).

### Sandbox
[Sandbox](https://github.com/algorand/sandbox) can run a private dev network separate from `goal`. The main advantage of this is that you don't have to sync to an actual network (can take tens of minutes even with Fast Catchup) and you can confirm blocks instantaneously on dev mode (instead of waiting ~4.5s). You can checkout an example in this very repo by running the script in `sandbox-scripts/sandbox-test.py`.
Sandbox commands are generally prefixed with `sandbox`, e.g. `sandbox goal account list`. 

## TEAL Contracts
[Compiling contracts using goal clerk](https://medium.com/algorand/understanding-algorand-smart-contracts-b9fc743e7a0f)

You can compile contracts using `goal clerk`

`goal clerk compile simple.teal -d ~/node/testnetdata`

You can also disassemble them and inspect it closer:
```
goal clerk compile subby.teal -d ~/node/testnetdata -o mysubbybin.tealc
goal clerk compile  -d ~/node/testnetdata -D mybin.tealc
```

Funnily enough, you always need to have a node running in order to compile a TEAL program (as of writing this). There is an example of how to do this using the Python SDK in `py-scripts`. You can supply a sandbox endpoint or a publicly available one (e.g. from the Developer's Academy) for ease of use.

### Stateless Contracts
[Docs here](https://developer.algorand.org/docs/features/asc1/stateless/). LogicSigs generally fall into this category. Stateless contracts do not read state from the blockchain, which means it is computationally cheaper to execute and has more op-code budget compared to stateful contracts.

### Stateful Contracts
[Tutorial here](https://developer.algorand.org/docs/features/asc1/stateful/hello_world)

### PyTeal
[Pyteal](https://github.com/algorand/pyteal) can generate TEAL code by using Python code.  Here is an example game that uses PyTeal to generate a smart contract to play Battleship: [AlgoShip](https://github.com/jasonpaulos/algoship).

You can also examine transactions on the Algorand blockchain (MainNet, TestNet, etc.) using [Algoexplorer](https://testnet.algoexplorer.io/). Try searching up your sample transaction by sender address and more!

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

#### Code reviews
You should have at least one person review your code/pull request before it is merged to master. The [Google Engineering guide](https://google.github.io/eng-practices/) is a good reference on how to give and address code reviews.

## Testing
Each repo has a set of unit tests and integration/end-to-end ("E2E") tests. But for your own sanity, you may wish to test your changes manually or live. 

### go-algorand
There are two ways you can manually test out a `go-algorand` build. 

1. Run `make install` locally. Your executable should be at `$GOPATH/bin` (you can also run `go env` to check where your `GOPATH` is). You can run `goal` commands from there. 
2. Use `sandbox` and make it point to a specific commit. Sandbox allows you to change the configs so that you can build an executable from a particular repo or branch. This also works for indexer changes. Feel free to refer to `sandbox-scripts/` in this repo for a script to help you get started. 

### SDKs
In addition to the individual tests in each repo (we currently support Go, Java, Python, and JavaScript/TypeScript), we have an [algorand-sdk-testing](https://github.com/algorand/algorand-sdk-testing) repo using Cucumber. This allows us to standardize the testing environment using Docker for all the SDKs and minimize copy-pasting the same tests again. 

Generally, each SDK has a Makefile that has tags, e.g. `@unit.transactions`, that allows tests to be toggled on/off for a particular SDK. For local testing, you can also run these tags individually, e.g. `behave --tags="@unit.transactions" test -f progress2` for the Python SDK. 

The Cucumber tests can be seen in `features/unit` or `features/integration` in the SDK testing repo.

## Indexer
Algod only keeps meaningful information about raw blocks (e.g. you query a block round and you get a JSON of all the information in that block). Algorand develops and maintains the [indexer](https://github.com/algorand/indexer) as a means of having a convenient way of making more meaningful queries on the blockchain state by maintaining its own Postgres database. It relies on an Algorand archival node (contains all the blocks in history) to validate transactions and imports them directly into its database. 

The indexer can be thought of as two components: a REST API handler and a backend that reads and writes from the database (ignoring some details like importing blocks and executing them in the ledger). You can probably use sandbox to test some commands directly, user curl or use the SDKs to interact with the APIs. There is a tutorial [here](https://developer.algorand.org/docs/get-details/indexer/).

## Teal Debugger (tealdbg)
`tealdbg` is a browser-based debugger that comes with `go-algorand`. There is a tutorial on how to use it in [`tealdbg-tutorial`](tealdbg-tutorial/README.md)
