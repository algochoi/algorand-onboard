#!/usr/bin/env bash

# You should generate an account on testnet before running this script...
# Testnet data is assumed to be in `~/node/testnetdata`
# Can get account using `goal account list -d ~/node/testnetdata`
ADDR=""

# Teal contract to approve any tx
echo "int 1" > simple.teal

# Compile and return contract address
goal clerk compile simple.teal -d ~/node/testnetdata

# Compile and sign
goal clerk compile simple.teal -o mydelegatedsig.lsig -s -a $ADDR -d ~/node/testnetdata

# Send 0.1 Algo from my account to my account (minus fees) using TEAL contract
goal clerk send -f $ADDR -a 10000 -t $ADDR -L mydelegatedsig.lsig -d ~/node/testnetdata
