from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/qr_metadata')
def gen_qr_code_metadata():
    # TODO: generate qr code
    pass


@app.route('/validate')
def validate():
    # TODO: validate qr code
    pass


@app.route('/vaccine', methods=['GET', 'POST'])
def view_or_add_vaccine_record():
    # TODO: GET - get a user's vaccine records
    # TODO: POST - create a user's vaccine records
    pass


if __name__ == '__main__':
    app.run()
