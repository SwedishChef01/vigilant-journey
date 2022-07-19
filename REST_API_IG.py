import numpy as np
import pandas as pd
import requests

def request(api_key, client_session_token, x_security_token):
    url = 'https://demo-api.ig.com/gateway/deal/session',
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'X-IG-API-KEY': api_key,
        'CST': client_session_token,
        'X-SECURITY-TOKEN': x_security_token,
        }
    r = requests.get(url, headers=headers)
    return url

# Login.
account = 'spreadbet'
identifier = 'gpjohno1'
password = 'Fly1ngF1sh!'
api_key = 'c6625d5036d679e7ca85095e12ceadd55b7b04a8'

login = {
    'url': 'https://demo-api.ig.com/gateway/deal/session',
    'headers': {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'VERSION': '2',
        'X-IG-API-KEY': api_key,
        },
    'credentials': {
        'identifier': identifier,
        'password': password,
        }
    }

r = requests.post(
    login['url'],
    headers=login['headers'],
    json=login['credentials']
    )

client_session_token = r.headers['CST']
x_security_token = r.headers['X-SECURITY-TOKEN']

# Accounts.
session = request(api_key, client_session_token, x_security_token)

# =============================================================================
# # Session.
# session = {
#     'url': 'https://demo-api.ig.com/gateway/deal/session',
#     'headers': {
#         'Content-Type': 'application/json; charset=UTF-8',
#         'Accept': 'application/json; charset=UTF-8',
#         'X-IG-API-KEY': api_key,
#         'CST': client_session_token,
#         'X-SECURITY-TOKEN': x_security_token,
#         }
#     }
# 
# r = requests.get(
#     session['url'],
#     headers=session['headers']
#     )
# =============================================================================

# =============================================================================
# # Watchlists.
# watchlists = {
#     'url': 'https://demo-api.ig.com/gateway/deal/watchlists/4193953',
#     'headers': {
#         'Content-Type': 'application/json; charset=UTF-8',
#         'Accept': 'application/json; charset=UTF-8',
#         'X-IG-API-KEY': api_key,
#         'CST': client_session_token,
#         'X-SECURITY-TOKEN': x_security_token,
#         }
#     }
# 
# r = requests.get(
#     watchlists['url'],
#     headers=watchlists['headers']
#     )
# =============================================================================
