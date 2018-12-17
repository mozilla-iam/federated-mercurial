-- Lua reference for nginx: https://github.com/openresty/lua-nginx-module
-- Lua reference for openidc: https://github.com/pingidentity/lua-resty-openidc
local cjson = require( "cjson" )
local jwt = require("lua-resty-jwt")

-- ngx.req.set_header("REMOTE_USER", session.data.user.email)
