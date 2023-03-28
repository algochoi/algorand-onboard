# Private networks

Private networks might be useful if you want to use a completely blank slate for testing.
This is the default for sandbox ("sandnet"), but you may want to replicate this on a node.

## Create a private devmode network

First, create a network template. There is a [Devmode network template](https://github.com/algorand/go-algorand/blob/master/test/testdata/nettemplates/DevModeNetwork.json) in go-algorand that we can use. Let's put that file in directory `~/net1` and `cd` into it.

Then, create the network:
```
./goal network create -r ~/net1 -n private -t DevModeNetwork.json
```
This will create the network directory in `~/net1`. In the `Node` directory inside `net1/`, there should be a `config.json`.
You can customize the configurations here.

Reference: https://developer.algorand.org/tutorials/create-private-network/

### Start network
Start up the network:
```
goal network start -r ~/net1
# Check network status
goal network status -r ~/net1
```
