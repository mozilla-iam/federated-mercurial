# -*- coding: utf-8 -*-
import base64
import json
import requests

# Import login library as its not yet available on pypi
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from login import login
from mercurial import extensions, httppeer, url, registrar

tokens = None


def extsetup(ui):
    extensions.wrapfunction(httppeer, "sendrequest", sendrequest)
    extensions.wrapfunction(url, "opener", opener)
    configtable = {}
    configitem = registrar.configitem(configtable)
    configitem("sso", "wellknownurl", default="https://auth.mozilla.auth0.com/.well-known/openid-configuration")
    configitem("sso", "clientid", default="WhSYI0qGKdtrB63gBjsdgN2qy69e79x8")
    configitem("sso", "scope", default="openid https://sso.mozilla.com/claim/groups")


def get_local_tokens(ui):
    global tokens
    ui.debug("sso.get_local_token: attempting to use cached token, if any\n")
    ## XXX actually add real file caching
    if tokens is not None:
        return tokens
    tokens = get_tokens(ui)
    id_token = json.loads(base64.b64decode(tokens["id_token"].split(".")[1] + "========="))
    ui.debug("sso.get_local_token: current id_token is set to expire at {}\n".format(id_token["exp"]))
    return tokens


def get_tokens(ui):
    client_id = ui.config("sso", "clientid")
    scope = ui.config("sso", "scope")
    wellknownurl = ui.config("sso", "wellknownurl")

    if client_id is None or scope is None or wellknownurl is None:
        ui.write(
            "sso extension settings are incorrect, make sure you have an [sso] section with clientid, scope and "
            "wellknownurl specified"
        )
        return None

    # Note, don't use requests.get(..).json() as this would require the simplejson import instead of just json
    oidc_config = json.loads(requests.get(wellknownurl).text)
    jwks = json.loads(requests.get(oidc_config["jwks_uri"]).text)

    ui.debug("sso.get_token: jwks retrieved, fetching token\n")

    tokens = login(oidc_config["authorization_endpoint"], oidc_config["token_endpoint"], client_id, scope)
    # Drop access token since we're not using it, just to be safe
    del tokens["access_token"]
    ui.debug("sso.get_token: retrieved tokens\n")
    return tokens


def opener(
    orig, ui, authinfo=None, useragent=None, loggingfh=None, loggingname=b"s", loggingopts=None, sendaccept=True
):
    opener = orig(ui, authinfo, useragent, loggingfh, loggingname, loggingopts, sendaccept)
    tokens = get_local_tokens(ui)
    if tokens is None:
        ui.debug("sso.opener: no tokens received! Push will probably fail due to missing authentication data")
    else:
        ui.debug("sso.opener: adding authorization header\n")
        opener.addheaders.append((r"Authorization", r"Bearer {}".format(tokens["id_token"])))
    return opener


def sendrequest(orig, ui, opener, req):
    tokens = get_local_tokens(ui)
    if tokens is None:
        ui.debug("sso.sendrequest: no tokens received! Push will probably fail due to missing authentication data")
    else:
        ui.debug("sso.sendrequest: adding authorization header\n")
        req.add_header("Authorization", "Bearer {}".format(tokens["id_token"]))
    return orig(ui, opener, req)
