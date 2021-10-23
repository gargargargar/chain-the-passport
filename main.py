from web3 import Web3
from flask import Flask

app = Flask(__name__)
url = "https://mainnet.infura.io/v3/5525aa496c284560a48cb2cd72fa634b"

@app.route('/')
def hello_world():
    w3 = Web3.HTTPProvider(url)
    return str(w3.isConnected())


if __name__ == '__main__':
    app.run()
