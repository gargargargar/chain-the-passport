import rsa
import base64
import json
from firebase_admin import auth, firestore


def _encrypt(text: str, public_key: rsa.PublicKey) -> str:
    cipher = rsa.encrypt(text.encode('utf8'), public_key)
    return base64.b64encode(cipher).decode('utf8')


def _decrypt(cipher: str, private_key: rsa.PrivateKey) -> str:
    text = rsa.decrypt(base64.b64decode(cipher.encode('utf8')), private_key)
    return text.decode('utf8')


def _validate_firebase_id_token(id_token: str) -> str:
    decoded_token = auth.verify_id_token(id_token)
    user_uid = decoded_token['uid']

    return user_uid


def gen_qr_code_metadata(id_token: str) -> str:
    # TODO: generate metadata with (address, vaccine_info) from blockchain
    # TODO: check if wallet number exists; if not, add it to firebase
    user_uid = _validate_firebase_id_token(id_token)
    if user_uid is None:
        return ''

    db = firestore.client()
    users_ref = db.collection(u'users')
    query_result = users_ref.where(u'uid', u'==', user_uid).stream()

    if not query_result:
        return ''

    user_ref = list(query_result)[0]
    user = user_ref.to_dict()

    if 'n' not in user:
        public_key, private_key = rsa.newkeys(512)
        user['n'] = str(public_key.n)
        user['e'] = str(public_key.e)
        user['d'] = str(private_key.d)
        user['p'] = str(private_key.p)
        user['q'] = str(private_key.q)

    metadata = {
        'address': '',  # blockchain
        'n': user['n'],
        'e': user['e'],
        'vaccine_info': '',  # decrypted from blockchain
        'user_uid': user_uid,
    }

    users_ref.document(user_ref.id).update(user)
    return json.dumps(metadata)


def validate_qr_code_metadata(qr_code_metadata: str) -> dict:
    metadata = json.loads(qr_code_metadata)

    metadata_keys = ['address', 'n', 'e', 'vaccine_info', 'user_uid']
    for key in metadata_keys:
        if key not in metadata:
            return {
                'validation_result': False,
                'name': None,
                'birthday': None,
            }

    return validate(metadata)


def validate(metadata: dict) -> dict:
    user_public_key = rsa.PublicKey(int(metadata['n']), int(metadata['e']))

    if not metadata['vaccine_info']:
        return {
            'validation_result': False,
            'name': 'Test',
            'birthday': '10/23',
        }

    decrypted_vaccine_info = _encrypt(
        metadata['vaccine_info'],
        user_public_key
    )

    # encrypted_vaccine_info_from_blockchain =
    # TODO get vaccine info from blockchain with metadata['transaction_id']



