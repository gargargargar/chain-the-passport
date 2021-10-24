from flask import Flask, request
import user
import json
import firebase_admin
import etherium

app = Flask(__name__)

default_app = firebase_admin.initialize_app()
etherium.initializeBlockchain()


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/qr_metadata')
def gen_qr_code_metadata():
    id_token = request.args.get('id_token')
    return user.gen_qr_code_metadata(id_token)


@app.route('/validate')
def validate():
    metadata = request.args.get('metadata')
    print(metadata)
    if metadata is None:
        metadata = json.dumps({})
    return user.validate_qr_code_metadata(metadata)


@app.route('/vaccine', methods=['GET', 'POST'])
def view_or_add_vaccine_record():
    # TODO: GET - get a user's vaccine records
    # TODO: POST - create a user's vaccine records
    return 'Work in progress'


if __name__ == '__main__':
    app.run(debug=True)

