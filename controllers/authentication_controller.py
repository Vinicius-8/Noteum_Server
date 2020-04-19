from google.oauth2 import id_token
from google.auth.transport import requests
import credentials


def auth_token(token) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), credentials.ANDROID_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            print('O login não foi autenticado pelo servidor')
            raise ValueError('Wrong issuer')
        # print('idinfo: {}'.format(idinfo))
        userid = idinfo['sub']
        return {'auth': True, 'userid': userid}
    except ValueError:
        print('Token Inválido')
        pass
    return {'auth': False}
