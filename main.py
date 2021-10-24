from flask import Flask, request
import user
import json
import firebase_admin
import etherium
import healthcare_worker

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
    if metadata is None:
        metadata = json.dumps({})
    return user.validate_qr_code_metadata(metadata)


@app.route('/vaccine', methods=['GET', 'POST'])
def view_or_add_vaccine_record():
    if request.method == 'GET':
        id_token = request.args.get('id_token')
        return healthcare_worker.get_vaccine_info(id_token)
    elif request.method == 'POST':
        request_body = request.form
        healthcare_worker.add_vaccine_record(request_body)

    return {}


if __name__ == '__main__':
    app.run(debug=True)

