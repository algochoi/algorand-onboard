# Teal Debugger Tutorial

## Pre-requisites
Make sure you have `go-algorand` checked out and ran `make install`. You should be able to run `tealdbg` from your terminal. This tutorial also uses `sandbox`, so make sure you have that as well. 

## Introduction
This document walks through some steps on using `tealdbg` using the Chrome Developer Tools (CDT) with stateful apps. We will use `sandbox` and the Python SDK instead of `goal` to execute some commands for simplicity's sake (imo). 

The included script, `tealdbg_deploy.py`, creates the app, then calls it in a group transaction where the first transaction is a payment to the app address and the second transaction is the app call. Then, it generates a debugger context using dryrun through `sandbox`. 

## Debugging a TEAL app
* Start `sandbox` if you haven't done so. Export `SANDBOX_PATH` pointing to your _sandbox_ directory.  Run the script to deploy the example app. The script will automatically save a `signed_txn.txn` file and the debugging context `dryrun_txn.msgp` in the `generated-data/`.
* Run `tealdbg`, e.g. from this directory, run: 
```tealdbg debug some_itxns.teal -d generated/data/dryrun_txn.msgp --group-index 1 -v```
* Open a Chrome based browser and go to: `chrome://inspect/#devices`. Press `Configure...` and add `127.0.0.1:9392`. This is the default port for tealdbg, but double check the tealdbg output to make sure this is the case.
* Open the CDT session either through Chrome or copying the link that is outputted on the tealdbg (it should start with `devtools://devtools`).
