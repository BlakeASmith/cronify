"""An intermediary between the local client application and the cronofy API OAuth service"""
from flask import Flask, request
import requests
import os
import json
from pathlib import Path
import time

# TODO: keep track of expiry and automatically request new token

with open(os.getenv('CLIENT_SECRETS_LOCATION'), 'r') as secrets:
    global SECRETS
    SECRETS = json.load(secrets)

client_id = 'hyGgyIY94QgUPsqs_dBDavKVm56R93VS'
scope = ['read_write']

def start(client_id, client_secret, scope)
    server_base_uri = 'http://localhost:5000'
    redirect_uri = f'{server_base_uri}/calendar-auth'

    app = Flask(__name__)

    client_tokens = {}

    @app.route('/auth/authurl/<identifier>', methods=['GET'])
    def make_auth_url(identifier):
        client_tokens[identifier] = None
        return (f'https://app.cronofy.com/oauth/authorize?response_type=code'
                f'&client_id={client_id}'
                f'&redirect_uri={redirect_uri}'
                f'&scope={"%20".join(scope)}'
                f'&state={identifier}')

    @app.route('/calendar-auth', methods=['GET'])
    def get_tokens():
        identifer = request.args.get('state') 
        assert identifer in client_tokens
        code = request.args.get('code')
        response = requests.post('https://api.cronofy.com/oauth/token', json={
                "client_id":client_id,
                "client_secret":SECRETS['client_secret'],
                "grant_type":"authorization_code",
                "code":code,
                "redirect_uri":redirect_uri
            })
        client_tokens[identifer] = response.json()

        return "<h1>Thanks! you can close the tab</h1>"

    @app.route('/auth/gettoken/<identifier>', methods=['GET'])
    def give_token_for_client(identifier):
        while not client_tokens[identifier]:
            time.sleep(0.1)
        return client_tokens[identifier]

    @app.route('/auth/gettoken/<identifier>/<refresh_token>')
    def refresh_token_for_user(identifier, refresh_token):
        response = requests.post('https://api.cronofy.com/oauth/token', json={
                "client_id":client_id,
                "client_secret":SECRETS['client_secret'],
                "grant_type":"refresh_token",
                "refresh_token":refresh_token
            })
        client_tokens[identifier] = response.json()
        return client_tokens[identifier]
    app.run(threaded=True)


if __name__ == '__main__':
    start(client_id, SECRETS['client_secret'], scope)


