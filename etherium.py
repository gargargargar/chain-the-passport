from solcx import compile_source
from web3 import Web3

contract = None
w3 = None


class Address:
    def __init__(self, address=None):
        global w3
        self.address = address or w3.eth.account.create().address


class Contract:
    def __init__(self, address=None, abi=None):
        url = "http://128.61.31.247:7545"
        global w3
        w3 = Web3(Web3.HTTPProvider(url))
        w3.eth.default_account = w3.eth.accounts[0]
        if address is None:
            self.newContract()
        else:
            global contract
            contract = w3.eth.contract(address = address, abi = abi)


    def newContract(self):
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
        Contract = w3.eth.contract(abi=abi, bytecode=byteCode)
        tx_hash = Contract.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        global contract
        contract = w3.eth.contract(address = tx_receipt.contractAddress, abi=abi)


def getString(address: str):
    address = Address(address=address)
    return contract.functions.getString(address.address).call() 


def setString(address: str, string: str):
    address = Address(address=address)
    tx_hash = contract.functions.updateString(address.address, string).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


def initializeBlockchain():
    c = Contract()


if __name__ == '__main__':
    initializeBlockchain()
    
    addr = Address()
    setString(addr.address, "Hello")
    print(getString(addr.address))
