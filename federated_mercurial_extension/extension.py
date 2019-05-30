# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base64
import requests
import json

from appdirs import user_data_dir
from federated_mercurial_extension.login import PkceLogin
from mercurial import extensions, httppeer, url, registrar

tokens = None
pkce = None

app_dir = user_data_dir("federated_mercurial_extension")
if not os.path.exists(app_dir):
    os.mkdir(app_dir)


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
    global pkce
    ui.debug("sso.get_local_token: attempting to use cached token, if any\n")
    if tokens is not None:
        return tokens
    tokens = get_tokens(ui)
    id_token = json.loads(base64.b64decode(tokens["id_token"].split(".")[1] + "========="))
    ui.debug("sso.get_local_token: current id_token is set to expire at {}\n".format(id_token["exp"]))
    return tokens


def get_tokens(ui):
    global app_dir
    global pkce
    client_id = ui.config("sso", "clientid")
    scope = ui.config("sso", "scope")
    wellknownurl = ui.config("sso", "wellknownurl")
    disk_cache_path = "{}/pkce_tokens".format(app_dir)

    if client_id is None or scope is None or wellknownurl is None:
        ui.write(
            "sso extension settings are incorrect, make sure you have an [sso] section with clientid, scope and "
            "wellknownurl specified"
        )
        return None

    ui.debug("sso.get_token: jwks retrieved, fetching token\n")
    if pkce is None:
        pkce = PkceLogin(wellknownurl, client_id, scope)
        ui.debug("sso.get_token: loading credentials from disk cache: {}\n".format(disk_cache_path))
        if os.path.isfile(disk_cache_path):
            with open(disk_cache_path) as fd:
                try:
                    pkce.tokens = json.load(fd)
                except ValueError:
                    ui.debug("sso.get_token: could not load disk cache")
                    os.unlink(disk_cache_path)

    pkce.refresh_id_token()
    ui.debug("sso.get_token: retrieved tokens\n")
    # Not P2 compat
    #    with open(os.open(disk_cache_path, os.O_CREAT | os.O_WRONLY, 0o600), "w+") as fd:
    os.umask(077)
    with open(disk_cache_path, "w+") as fd:
        json.dump(pkce.tokens, fd)
        ui.debug("sso.get_token: saved tokens to disk cache: {}\n".format(disk_cache_path))
    return pkce.tokens


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
