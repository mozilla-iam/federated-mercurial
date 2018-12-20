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
- `discovery_url`: The OpenID Connect discovery URL, used to find the issuer, public key to verify against, etc.
- `client_id`: Your OpenID Connect client id, used to verify the audience.

## Testing

Once running you can test like this:

```
$ token="a valid jwt token, you can find one on jwt.io for example"
$ curl -H "Authorization: Bearer $token" http://localhost:8080
```
