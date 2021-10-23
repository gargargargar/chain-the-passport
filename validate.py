import rsa
import base64
import json


def _encrypt(text: str, public_key: rsa.PublicKey) -> str:
    cipher = rsa.encrypt(text.encode('utf8'), public_key)
    return base64.b64encode(cipher).decode('utf8')


def _decrypt(cipher: str, private_key: rsa.PrivateKey) -> str:
    text = rsa.decrypt(base64.b64decode(cipher.encode('utf8')), private_key)
    return text.decode('utf8')


def gen_qr_code_metadata(session_id: str) -> str:
    # TODO: generate metadata with {block_record_id, user_public_key, encrypted_vaccine_info} from blockchain
    metadata = {
        'transaction_id': '',  # blockchain
        'user_public_key': '',  # firebase
        'encrypted_vaccine_info': '',  # blockchain
    }
    return json.dumps(metadata)


def validate_qr_code_metadata(qr_code_metadata):
    metadata = json.loads(qr_code_metadata)

    metadata_keys = ['transaction_id', 'user_public_key', 'encrypted_vaccine_info']
    for key in metadata_keys:
        if key not in metadata:
            return False

    return validate(metadata)


def validate(metadata: dict) -> bool:
    decrypted_vaccine_info = _decrypt(
        metadata['encrypted_vaccine_info'],
        metadata['user_public_key']
    )

    # encrypted_vaccine_info_from_blockchain =
    # TODO get vaccine info from blockchain with metadata['transaction_id']

    return True

