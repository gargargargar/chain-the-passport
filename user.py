import rsa
import base64
import json
import etherium
from firebase_admin import auth, firestore


def encrypt(text: str, public_key: rsa.PublicKey) -> str:
    # cipher = rsa.encrypt(text.encode('utf8'), public_key)
    # return base64.b64encode(cipher).decode('utf8')
    return text


def decrypt(cipher: str, private_key: rsa.PrivateKey) -> str:
    # text = rsa.decrypt(base64.b64decode(cipher.encode('utf8')), private_key)
    # return text.decode('utf8')
    return cipher


def validate_firebase_id_token(id_token: str) -> str:
    decoded_token = auth.verify_id_token(id_token)
    user_uid = decoded_token['uid']

    return user_uid


def gen_qr_code_metadata(id_token: str) -> str:
    user_uid = validate_firebase_id_token(id_token)
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

    if 'address' not in user:
        address = etherium.Address()
        user['address'] = address.address

    try:
        vaccine_info = etherium.getString(user['address'])
    except:
        return ''

    metadata = {
        'address': user['address'],
        'n': user['n'],
        'e': user['e'],
        'vaccine_info': vaccine_info,
        'user_uid': user_uid,
    }

    users_ref.document(user_ref.id).update(user)
    return json.dumps(metadata)


def validate_qr_code_metadata(qr_code_metadata: str) -> dict:
    metadata = json.loads(qr_code_metadata)

    metadata_keys = ['address', 'n', 'e', 'vaccine_info']
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
            'name': '',
            'birthday': '',
        }

    encrypted_vaccine_info = encrypt(
        metadata['vaccine_info'],
        user_public_key
    )

    encrypted_vaccine_info_from_blockchain = etherium.getString(metadata['address'])
    if encrypted_vaccine_info == encrypted_vaccine_info_from_blockchain:
        # valid vaccination information
        vaccine_info_dict = json.loads(metadata['vaccine_info'])
        return {
            'validation_result': True,
            'name': vaccine_info_dict.get('first_name', '') + ' ' + vaccine_info_dict.get('last_name', ''),
            'birthday': vaccine_info_dict.get('birth_month', '') + '/' + vaccine_info_dict.get('birth_date', ''),
        }

    return {
        'validation_result': False,
        'name': '',
        'birthday': '',
    }



