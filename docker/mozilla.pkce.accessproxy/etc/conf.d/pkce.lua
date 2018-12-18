-- Lua reference for nginx: https://github.com/openresty/lua-nginx-module
-- Lua reference for openidc: https://github.com/pingidentity/lua-resty-openidc
-- Lua reference for jwt: https://github.com/SkyLothar/lua-resty-jwt
local cjson = require( "cjson" )
local jwt = require("lua-resty-jwt")

-- ngx.req.set_header("REMOTE_USER", session.data.user.email)
