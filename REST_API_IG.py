'''IG Markets REST trading API.'''

import numpy as np
import os
import pandas as pd
import requests


def get(endpoint):
    '''Response for GET HTTP request.'''
    url = f'https://demo-api.ig.com/gateway/deal/{endpoint}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'X-IG-API-KEY': API_KEY,
        'CST': cst,
        'X-SECURITY-TOKEN': xst,
    }
    response = requests.get(url, headers=headers).json()
    return response


def login():
    '''Create a trading session and return session tokens.'''
    url = 'https://demo-api.ig.com/gateway/deal/session'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'VERSION': '2',
        'X-IG-API-KEY': API_KEY,
    }
    credentials = {
        'identifier': IDENTIFIER,
        'password': PASSWORD,
    }
    response = requests.post(url, headers=headers, json=credentials)
    client_session_token = response.headers['CST']
    x_security_token = response.headers['X-SECURITY-TOKEN']
    return client_session_token, x_security_token


# Credentials.
API_KEY = os.environ.get('API_KEY_IG_DEMO')
IDENTIFIER = os.environ.get('IDENTIFIER_IG')
PASSWORD = os.environ.get('PASSWORD_IG')

# Login
cst, xst = login()

# Accounts.
accounts = get('accounts')
