import json
from solcx import compile_source
from web3 import Web3

contract = None
w3 = None

class User:
    def __init__(self):
        global w3
        self.address = w3.eth.account.create().address

def getString(account):
    return contract.functions.getString(account.address).call() 

def setString(account, string):
    tx_hash = contract.functions.updateString(account.address, string).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
   
    
def initializeBlockchain():
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
    url = "http://127.0.0.1:7545"
    global w3
    w3 = Web3(Web3.HTTPProvider(url))
    w3.eth.default_account = w3.eth.accounts[0]
    Contract = w3.eth.contract(abi=abi, bytecode=byteCode)
    tx_hash = Contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    global contract
    contract = w3.eth.contract(address = tx_receipt.contractAddress, abi=abi)



if (__name__ == '__main__'): 

    initializeBlockchain()
    account1 = User()
    account2 = User()
    setString(account1, "String")
    setString(account2, "String2")
    print(getString(account2))
    print(getString(account1))