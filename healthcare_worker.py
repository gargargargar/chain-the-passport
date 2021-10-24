import json
import user
import rsa
import etherium
from firebase_admin import firestore


def get_vaccine_info(id_token: str) -> dict:
    db = firestore.client()
    user_uid = user.validate_firebase_id_token(id_token)

    users_ref = db.collection(u'users')
    query_result = users_ref.where(u'uid', u'==', user_uid).stream()

    if not query_result:
        return {}

    user_ref = list(query_result)[0]
    user_dict = user_ref.to_dict()

    encrypted_vaccine_info = etherium.getString(user_dict['address'])
    vaccine_info_str = user.decrypt(encrypted_vaccine_info, rsa.PrivateKey(
        int(user_dict['n']), int(user_dict['e']), int(user_dict['d']), int(user_dict['p']), int(user_dict['q'])))

    return json.loads(vaccine_info_str)


def add_vaccine_record(request_body: dict):
    db = firestore.client()
    qr_code_metadata = request_body.get('metadata', '{}')
    metadata = json.loads(qr_code_metadata)

    if 'uid' not in metadata:
        return
    user_uid = metadata['uid']

    users_ref = db.collection(u'users')
    query_result = users_ref.where(u'uid', u'==', user_uid).stream()

    if not query_result:
        return

    user_ref = list(query_result)[0]
    user_dict = user_ref.to_dict()

    if 'address' not in user_dict:
        address = etherium.Address()
        user_dict['address'] = address.address
        users_ref.document(user_ref.id).update(user_dict)

    vaccine_info = {
        'first_name': request_body.get('first_name', ''),
        'last_name': request_body.get('last_name', ''),
        'birth_year': request_body.get('birth_year', ''),
        'birth_month': request_body.get('birth_month', ''),
        'birth_date': request_body.get('birth_date', ''),
        'product_name': request_body.get('product_name', ''),
        'lot_number': request_body.get('lot_number', ''),
        'year': request_body.get('year', ''),
        'month': request_body.get('month', ''),
        'date': request_body.get('date', ''),
        'site': request_body.get('site', ''),
        'first_or_second_dose': request_body.get('first_or_second_dose', 'first'),
    }

    vaccine_info_str = json.dumps(vaccine_info)
    encrypted_vaccine_info = user.encrypt(vaccine_info_str, rsa.PublicKey(int(user_dict['n']), int(user_dict['e'])))
    etherium.setString(user_dict['address'], encrypted_vaccine_info)
