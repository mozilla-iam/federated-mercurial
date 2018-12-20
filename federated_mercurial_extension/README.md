# Mercurial Federated Extension (SSO)

This is a proof of concept extension which adds SSO/IAM federation to Mercurial, when the server side of mercurial is
setup with a JWT Access Proxy.

This extension performs a PKCE authentication flow and insert the authorization token in the request headers by wrapping
the `sendrequest` function (from httppeer).
This function has been selected after inspecting the output of `python2 -m trace --listfunc hg push http://localhost:8000/test`

## TODO

- Add file caching of the token (so that the session itself is cached for the token lifetime)

## Configuration

In order to use this extension, place it with it's relevant files somewhere such as `~/.hgext`.
Edit `~/.hgrc` and add something like this:

```
...
[extensions]
sso=~/.hgrc/sso/extension.py

[sso]
wellknownurl=https://auth.mozilla.auth0.com/.well-known/openid-configuration
clientid=WhSYI0qGKdtrB63gBjsdgN2qy69e79x8
scope=openid https://sso.mozilla.com/claim/groups
```

NOTE: These are the values used for Mozilla IAM. `clientid` is a public string. The well-known URL is an OpenID Connect
well-known URL. The `clientid` is an OAuth2 identifier and the `scope` is an OAuth2 `scope` for OpenID Connect (yours
may be `openid profile`)
