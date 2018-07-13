import logging
import jwt
from django.conf import settings


def jwt_encode(payload):
    """
    Encode jwt by payload
    :param payload: type: dict, the data to be encoded
    :return: type: str, the result
    """
    try:
        key = settings.LOGIN_SECRET
        encoded_bytes = jwt.encode(payload, key, algorithm='HS256')
        encoded = bytes.decode(encoded_bytes)
    except Exception:
        logging.error("jwt encode error, for payload={}".format(payload))
        return None
    return encoded


def jwt_decode(encoded_data):
    """
    Decode the data of encoded_data
    :param encoded_data: str, the encoded string
    :return: dict, the data
    """
    try:
        key = settings.LOGIN_SECRET
        payload = jwt.decode(encoded_data, key)
    except Exception:
        logging.error("jwt decode error, for encoded_data={}".format(encoded_data))
        return None
    return payload
