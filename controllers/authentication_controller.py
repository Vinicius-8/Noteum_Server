from google.oauth2 import id_token
from google.auth.transport import requests
from os import environ


def auth_token(token) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), environ.get('ANDROID_CLIENT_ID'))
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            print('O login não foi autenticado pelo servidor')
            raise ValueError('Wrong issuer')
        # print('idinfo: {}'.format(idinfo))
        return {'auth': idinfo['email_verified'], 'userid': idinfo['sub'], 'email': idinfo['email']}
    except ValueError:
        print('Token Inválido')
    return {'auth': False}
