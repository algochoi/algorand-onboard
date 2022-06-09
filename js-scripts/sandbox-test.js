const algosdk = require('algosdk');

// Sandbox accounts
// ./sandbox goal account list
// ./sandbox goal account export -a <address_of_funded_account>
const sandboxAddr =
  'LANYGPIMGF3G52ROPIXK5NYATK2SV6NBPBJTTYMGB3SZOD3OSAA4KAA2NU';
const mnemonic =
  'unknown catalog minimum link fork sound talk usage lesson scene job buffalo trophy clog horror glue nothing situate thrive evil weapon phone forum about media';
const sandboxAccount = algosdk.mnemonicToSecretKey(
  'unknown catalog minimum link fork sound talk usage lesson scene job buffalo trophy clog horror glue nothing situate thrive evil weapon phone forum about media'
);

// Compile Program
async function getBasicProgramBytes(client) {
  const program = '#pragma version 2\nint 1';

  // use algod to compile the program
  const compiledProgram = await client.compile(program).do();
  return new Uint8Array(Buffer.from(compiledProgram.result, 'base64'));
}

// Create an account and add funds to it. Copy the address off
// The Algorand TestNet Dispenser is located here:
// https://dispenser.testnet.aws.algodev.network/
const createAccount = function () {
  try {
    const myaccount = algosdk.generateAccount();
    console.log('Account Address = ' + myaccount.addr);
    let account_mnemonic = algosdk.secretKeyToMnemonic(myaccount.sk);
    console.log('Account Mnemonic = ' + account_mnemonic);
    console.log('Account created. Save off Mnemonic and address');
    console.log('Add funds to account using the TestNet Dispenser: ');
    console.log('https://dispenser.testnet.aws.algodev.network/ ');

    return myaccount;
  } catch (err) {
    console.log('err', err);
  }
};

function createClient() {
  // Connect your client
  const algodToken =
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
  const algodServer = 'http://localhost';
  const algodPort = 4001;
  return new algosdk.Algodv2(algodToken, algodServer, algodPort);
}

async function firstTransaction() {
  try {
    const myAccount = sandboxAccount;
    const algodClient = createClient();

    //Check your balance
    let accountInfo = await algodClient.accountInformation(myAccount.addr).do();
    console.log('Account balance: %d microAlgos', accountInfo.amount);

    // Construct the transaction
    let params = await algodClient.getTransactionParams().do();
    // comment out the next two lines to use suggested fee
    params.fee = algosdk.ALGORAND_MIN_TX_FEE;
    params.flatFee = true;

    // receiver defined as TestNet faucet address
    const receiver =
      'HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA';
    const enc = new TextEncoder();
    const note = enc.encode('Hello World');
    let amount = 1000000;
    let sender = myAccount.addr;
    let txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: sender,
      to: receiver,
      amount: amount,
      note: note,
      suggestedParams: params,
    });

    // Sign the transaction
    let signedTxn = txn.signTxn(myAccount.sk);
    let txId = txn.txID().toString();
    console.log('Signed transaction with txID: %s', txId);

    // Submit the transaction
    await algodClient.sendRawTransaction(signedTxn).do();

    // Wait for confirmation
    let confirmedTxn = await algosdk.waitForConfirmation(algodClient, txId, 4);
    //Get the completed Transaction
    console.log(
      'Transaction ' +
        txId +
        ' confirmed in round ' +
        confirmedTxn['confirmed-round']
    );
    let string = new TextDecoder().decode(confirmedTxn.txn.txn.note);
    console.log('Note field: ', string);
    accountInfo = await algodClient.accountInformation(myAccount.addr).do();
    console.log('Transaction Amount: %d microAlgos', confirmedTxn.txn.txn.amt);
    console.log('Transaction Fee: %d microAlgos', confirmedTxn.txn.txn.fee);

    console.log('Account balance: %d microAlgos', accountInfo.amount);
  } catch (err) {
    console.log('err', err);
  }
  process.exit();
}

firstTransaction();
