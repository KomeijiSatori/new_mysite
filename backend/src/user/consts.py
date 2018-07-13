# login cookie related
"""
for cookie USER_TOKEN_COOKIE_NAME, after jwt decode, the data will be
{
    USER_TOKEN_USER_ID_NAME: "1",
    USER_TOKEN_VALID_TOKEN_NAME: "qwertyuiop"
}

for redis check hset USER_TOKEN_HSET_NAME
key: user_id
value: "{REDIS_TOKEN_VALID_TOKEN_NAME: "qwertyuiop", REDIS_TOKEN_EXPIRE_TIME_NAME: "153459090"}"
"""

USER_TOKEN_COOKIE_NAME = "user_token"
USER_TOKEN_USER_ID_NAME = "id"
USER_TOKEN_VALID_TOKEN_NAME = "token"
USER_TOKEN_HSET_NAME = "user_token"
REDIS_TOKEN_VALID_TOKEN_NAME = "token"
REDIS_TOKEN_EXPIRE_TIME_NAME = "expire_time"

USER_CACHE_HSET_NAME = "user"
