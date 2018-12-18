# JWT Access Proxy

This is nothing more than a reverse-proxy that validates JWT coming from an OAuth2 implementation (such as Auth0's).
It uses https://github.com/cdbattags/lua-resty-jwt/ and OpenResty. It supports passing configuration via environment and [`credstash`](https://github.com/fugue/credstash).

It is originally based on https://github.com/mozilla-iam/mozilla.oidc.accessproxy

## Setup

Pass these environment variable or store them in credstash:

- `backend`: URL to the origin/backend server
- `httpsredir`: Set to true in order to enable automatic HTTPS redirection (recommended)
- `allowed_group`: The list of groups that are allowed to get in. This will check the JWT for a `groups` or similar
  claim.
- `jwt_pub_key`: The PEM formatted public key that JWT's can be verified with. If the OAuth2 server signing JWTs also
  supports OpenID Connect, you can usually find this in the discovery URL's JWKS (it's the `x5c` parameter). Note that
the line feeds ("\n") are required.

## Testing

Once running you can test like this:

```
$ token="a valid jwt token, you can find one on jwt.io for example"
$ curl -H "Authorization: Bearer $token" http://localhost:8080
```
