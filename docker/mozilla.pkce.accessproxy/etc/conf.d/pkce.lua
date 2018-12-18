local cjson = require "cjson"
local jwt = require "resty.jwt"
local validators = require "resty.jwt-validators"

local jwt_token = ngx.var.arg_jwt
local auth_header = ngx.var.http_Authorization
if auth_header then
  _, _, jwt_token = string.find(auth_header, "Bearer%s+(.+)")
end

-- jwt_pub_key is set in the environment is and is a PEM formatted string
local jwt_pub_key = os.getenv("jwt_pub_key")
jwt_pub_key = jwt_pub_key:gsub("\\n", "\n")

ngx.header.content_type = "application/json; charset=utf-8"

local claimspec = {
  validators.set_system_leeway(60), -- seconds
  exp = validators.is_not_expired(),
  iat = validators.is_not_before(),
  iss = validators.equals_any_of({ "https://auth.mozilla.auth0.com/", "https://auth-dev.mozilla.auth0.com/" }),
--  https://sso.mozilla.com/claim/groups = validators.opt_matches("") -- Mozilla group structure
}

if not jwt_pub_key then
  ngx.log(ngx.WARN, "no jwt public key, make sure you have set jwt_pub_key")
  ngx.status = ngx.HTTP_UNAUTHORIZED
  ngx.say("{\"error\": \"server misconfigured\"}")
  ngx.exit(ngx.HTTP_UNAUTHORIZED)

elseif not jwt_token then
  ngx.log(ngx.WARN, "no JWT token found")
  ngx.status = ngx.HTTP_UNAUTHORIZED
  ngx.say("{\"error\": \"missing JWT token or Authorization header\"}")
  ngx.exit(ngx.HTTP_UNAUTHORIZED)

else
-- ngx.req.set_header("REMOTE_USER", session.data.user.email)
  local jwt_obj = jwt:verify(jwt_pub_key, jwt_token)
  if not jwt_obj.verified then
    ngx.log(ngx.WARN, "JWT verification failure:" .. jwt_obj.reason)
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say("{\"error\": \"" .. jwt_obj.reason .. "\"}")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
  end

  ngx.log(ngx.NOTICE, "JWT token verified successfully")
  ngx.say(cjson.encode(jwt_obj));
  ngx.exit(ngx.HTTP_OK)
end
