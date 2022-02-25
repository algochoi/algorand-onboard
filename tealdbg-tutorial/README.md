# Teal Debugger Tutorial

## Pre-requisites
Make sure you have `go-algorand` checked out and ran `make install`. You should be able to run `tealdbg` from your terminal. This tutorial also uses `sandbox`, so make sure you have that as well. 

## Introduction
This document walks through some steps on using `tealdbg` using the Chrome Developer Tools (CDT) with stateful apps. We will use `sandbox` and the Python SDK instead of `goal` to execute some commands for simplicity's sake. 

The included script, `tealdbg_deploy.py`, creates the app, then calls it in a group transaction where the first transaction is a payment to the app address and the second transaction is the app call. Then, it generates a debugger context using dryrun through `sandbox`. 

To install the dependencies, run:
```
pip install -r requirements.txt
```

## Debugging a TEAL app
* Start `sandbox` if you haven't done so. Export `SANDBOX_PATH` pointing to your _sandbox_ directory, i.e. `export SANDBOX_PATH="your-path-to-sandbox-directory"`.
* Run the script to deploy the example app. The script will automatically save a `signed_txn.txn` file and the debugging context `dryrun_txn.msgp` in the `generated-data/`.
* Run `tealdbg`, e.g. from this directory, run: 

```
tealdbg debug some_itxns.teal -d generated/data/dryrun_txn.msgp --group-index 1 -v
```

* Open a Chrome based browser and go to: `chrome://inspect/#devices`. Press `Configure...` and add `127.0.0.1:9392`. This is the default port for tealdbg, but double check the tealdbg output to make sure this is the case.
* Open the CDT session either through Chrome or copying the link that is outputted on the tealdbg (it should start with `devtools://devtools`).

### Debugging grouped transactions
You can run a group of transaction by supplying the dryrun dump or a transaction group (encoded in `msgp`) with the balances file. e.g. `tealdbg debug -d dryrun_grp_.msgp` will allow you to debug each transaction in the group with a separate CDT tab. 

Note that certain ops such as `gload` will only work when the entire group is supplied. Currently the `gaid` op is not supported by tealdbg. 
