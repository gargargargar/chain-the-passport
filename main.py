from flask import Flask, request
import user
import json

app = Flask(__name__)
url = "https://mainnet.infura.io/v3/5525aa496c284560a48cb2cd72fa634b"

@app.route('/')
def hello_world():
    w3 = Web3.HTTPProvider(url)
    return str(w3.isConnected())


@app.route('/qr_metadata')
def gen_qr_code_metadata():
    session_id = request.args.get('session_id')
    return user.gen_qr_code_metadata(session_id)


@app.route('/validate')
def validate():
    metadata = request.args.get('metadata')
    if metadata is None:
        metadata = json.dumps({})
    return user.validate_qr_code_metadata(metadata)


@app.route('/vaccine', methods=['GET', 'POST'])
def view_or_add_vaccine_record():
    # TODO: GET - get a user's vaccine records
    # TODO: POST - create a user's vaccine records
    return 'Work in progress'


if __name__ == '__main__':
    app.run()
