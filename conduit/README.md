# Let's start Conduit!

## Pre-requisites
* Install an algod node. See this for more details: https://developer.algorand.org/docs/run-a-node/setup/install/

## Install Conduit
```
git clone https://github.com/algorand/conduit.git
cd conduit
make
# Conduit will be installed at cmd/conduit/conduit
```
Reference: https://github.com/algorand/conduit

## Start up algod on testnet
First make sure that the algod has `EnableFollowMode: true` in the `config.json`. This should pause catchup. Then start up algod by using some variant of `goal node start`.

Follow mode should pause the node at a particular round. 

You can advance blocks by setting the sync round using the `POST /v2/ledger/sync/{round}` endpoint, e.g.

```
# assuming data directory is in ~/node/data
curl -i -X POST -H "X-Algo-API-Token: $(cat ~/node/data/algod.token)" http://$(cat ~/node/data/algod.net)/v2/ledger/sync/24410187
```

Reference: https://github.com/algorand/go-algorand/blob/master/docs/follower_node.md

## Start up Conduit
Start up Conduit and initialize the `data` directory:
```
conduit init
cd data
# change algod url and token in config.yml
cd ..
conduit -d data
```
