'''IG Markets REST trading API.'''

import numpy as np
import pandas as pd
import requests


def request(endpoint):
    '''Response for GET HTTP request.'''
    url = f'https://demo-api.ig.com/gateway/deal/{endpoint}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'X-IG-API-KEY': API_KEY,
        'CST': tokens['client_session_token'],
        'X-SECURITY-TOKEN': tokens['x_security_token'],
        }
    response = requests.get(url, headers=headers)
    return response


def login():
    '''Create trading session and return session tokens.'''
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
    tokens = {
        'client_session_token': response.headers['CST'],
        'x_security_token': response.headers['X-SECURITY-TOKEN'],
        }
    return tokens

# Constants.
API_KEY = 'c6625d5036d679e7ca85095e12ceadd55b7b04a8'
IDENTIFIER = 'gpjohno1'
PASSWORD = 'Fly1ngF1sh!'

# Login
tokens = login()

# Accounts.
accounts = request('accounts').json()
