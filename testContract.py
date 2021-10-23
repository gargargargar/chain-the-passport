import json
from solcx import compile_source
from web3 import Web3
if (__name__ == '__main__'): 
    compiled_sol = compile_source(
    '''
    pragma solidity 0.4.25;

    contract Passport {
    
        mapping(address => string) public table;
    
        constructor() {
        
        }
    
        function updateString(address recipient, string memory newString) public {
            table[recipient] = newString;
        }
    
        function getString(address recipient) public returns (string memory) {
            return table[recipient];
        }
    
        }
    ''')

    contractInterface = compiled_sol.popitem()
    byteCode = contractInterface[1]['bin']
    abi = contractInterface[1]['abi']
    url = "http://127.0.0.1:8545"
    w3 = Web3(Web3.HTTPProvider(url))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.isConnected())

    Passport = w3.eth.contract(abi=abi, bytecode=byteCode)

    tx_hash = Passport.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    account_1 = "0x8e7Be43b3721B63032C0F38582CedbAC7F8b00AA"
    account_2 = "0x24962e7c1Ac1FfC3FAA904468B3A814F7eb8d23e"
    private_key = "0xc52f018f701db0a00095ee20c907cd2560cb982e38b9eebac97fc203cd89c67d"
    passport = w3.eth.contract(address = tx_receipt.contractAddress, abi=abi)
    #tx_hash1 = passport.functions.updateString("0x24962e7c1Ac1FfC3FAA904468B3A814F7eb8d23e", "String").transact()
    #tx_receipt1 = w3.eth.wait_for_transaction_receipt(tx_hash1)
    print(passport.functions.getString("0x24962e7c1Ac1FfC3FAA904468B3A814F7eb8d23e").call())
    nonce = w3.eth.getTransactionCount(account_1)

    transaction = {
        'nonce': nonce,
        'to': account_2,
        'value': w3.toWei(1, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }

    signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
    hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(hash)

    
    #abi = json.loads('[{"inputs": [{"internalType": "uint256","name": "num","type": "uint256"}],"name": "store","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "retrieve","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"}]')
    #address = w3.toChecksumAddress("0xd9145CCE52D386f254917e481eB44e9943F39138")
    #contract = w3.eth.contract(address=address,abi=abi)
    
    #print(contract.functions.retrieve().call())