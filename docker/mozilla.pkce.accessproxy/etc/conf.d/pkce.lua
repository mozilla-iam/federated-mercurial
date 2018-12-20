-- Vars
local cjson = require "cjson"
local cjson_s = require "cjson.safe"
local http = require "resty.http"
local jwt = require "resty.jwt"
local validators = require "resty.jwt-validators"

local auth_header = ngx.var.http_Authorization
local jwt_token = nil
if auth_header then
  _, _, jwt_token = string.find(auth_header, "Bearer%s+(.+)")
else
  ngx.log(ngx.WARN, "No authentication header found!")
  ngx.status = ngx.HTTP_UNAUTHORIZED
  ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- Funcs
local function get_url_json(url)
  local json, err
  local httpc = http.new()
  local res, error = httpc:request_uri(url)
  if not res then
    err = "accessing url (" .. url .. ") failed: " .. error
  else
    json = cjson_s.decode(res.body)
  end

  return json, err
end

local function split_by_chunk(text, chunkSize)
  local s = {}
  for i = 1, #text, chunkSize do
    s[#s + 1] = text:sub(i, i + chunkSize - 1)
  end
  return s
end

local function base64_url_decode(input)
  local reminder = #input % 4
  if reminder > 0 then
    local padlen = 4 - reminder
    input = input .. string.rep('=', padlen)
  end
  input = input:gsub('-', '+'):gsub('_', '/')
  return ngx.decode_base64(input)
end

local function pem_from_x5c(x5c)
  local chunks = split_by_chunk(ngx.encode_base64(base64_url_decode(x5c[1])), 64)
  local pem = "-----BEGIN CERTIFICATE-----\n" ..
      table.concat(chunks, "\n") ..
      "\n-----END CERTIFICATE-----"
  return pem
end

-- Dynamic vars
local client_id = os.getenv("client_id")
local discovery_url = os.getenv("discovery_url")
local discovery, err = get_url_json(discovery_url)
local issuer = discovery.issuer
local jwks, err = get_url_json(discovery.jwks_uri)
-- Remember, lua tables starts at 1, not 0.
local jwt_pub_key = pem_from_x5c(jwks.keys[1].x5c)

ngx.header.content_type = "application/json; charset=utf-8"

-- Actual JWT verification
local claimspec = {
  validators.set_system_leeway(60), -- seconds
  exp = validators.is_not_expired(),
  iat = validators.is_not_before(),
  iss = validators.equals_any_of({ issuer }),
  aud = validators.equals_any_of({ client_id } ), -- The client id / our audience, this is as important as `iss`
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
    ngx.log(ngx.ERR, cjson.encode(jwt_obj))
    ngx.log(ngx.WARN, "JWT verification failure: " .. jwt_obj.reason)
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say("{\"error\": \"" .. jwt_obj.reason .. "\"}")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
  end

  ngx.log(ngx.NOTICE, "JWT token verified successfully")
  ngx.say(cjson.encode(jwt_obj));
  ngx.exit(ngx.HTTP_OK)
end
