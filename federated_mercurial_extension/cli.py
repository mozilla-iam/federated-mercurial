# -*- coding: utf-8 -*-

import base64
import json
import logging
import requests
import time
import platform

from login import login

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def do_login(config):
    tokens = login(config['openid-configuration']['authorization_endpoint'],
                   config['openid-configuration']['token_endpoint'],
                   config['client_id'],
                   config['scope'])
    logger.debug(tokens)
    return tokens


def main():
    logger.setLevel(logging.DEBUG)

    config = {}
    config['well-known_url'] = 'https://auth.mozilla.auth0.com/.well-known/openid-configuration'
    config['client_id'] = 'WhSYI0qGKdtrB63gBjsdgN2qy69e79x8'
    config['scope'] = 'openid https://sso.mozilla.com/claim/groups'


    config['openid-configuration'] = requests.get(config['well-known_url']).json()
    config['jwks'] = requests.get(config['openid-configuration']['jwks_uri']).json()
    logger.debug('config : {}'.format(config))

    tokens = do_login(config)
    # JWT will be verified by the server side - we just need to parse it
    # JWT b64 is not padded so we arbitrarily pad it back
    id_token = json.loads(base64.b64decode(tokens['id_token'].split('.')[1]+'========='))
    logger.debug('id_token: {}'.format(id_token))
    logger.debug('id_token will expire at {}'.format(id_token['exp']))


if __name__ == "__main__":
    main()
