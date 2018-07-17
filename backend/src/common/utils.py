from datetime import datetime, timedelta
import random
import json
import django_redis
from django.http import JsonResponse

from .consts import get_return_message

# common utils
def get_current_timestamp():
    now = datetime.now()
    return now.timestamp()

def get_timestamp_from_now(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    now = datetime.now()
    time_delta = timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=microseconds, minutes=minutes, hours=hours, weeks=weeks)
    target_time = now + time_delta
    return target_time.timestamp()


# redis utils
def get_redis_connection():
    conn = django_redis.get_redis_connection("default")
    return conn

def redis_hget(key, field):
    conn = get_redis_connection()
    return conn.hget(key, field)

def redis_hset(key, field, value):
    conn = get_redis_connection()
    conn.hset(key, field, value)

def redis_hdel(key, field):
    conn = get_redis_connection()
    conn.hdel(key, field)


# request parameter utils
def get_params(request):
    """
    Get the params of get method, raise exception if error occurs
    """
    params = request.GET.dict()
    return params

def post_params(request):
    """
    Get the params of get method, raise exception if error occurs
    """
    params = json.loads(request.body.decode("utf-8"))
    return params

# check and transform the type of parameters described in attrs, use dict to describe object and list for a set of objects
# using require to judge if a type of attrs can be None
# return the formatted patameters, through exception if meets transform error

# S is the start symbol, SEG is segments, ATTR is the name of key words, Type is the type , REQ is a boolean flag

# S -> { SEG }
# SEG -> SEG, SEG
# SEG -> ATTR: {"type": TYPE, "required": REQ}
# TYPE -> int | str
# TYPE -> { SEG }
# TYPE -> [TYPE]
#
# ATTR -> "[a-z_]+"
# REQ -> True | False
#
# Examples
# params = {"one": [{"two": "2", "three": ["3", 3]}], "four": {"five": "5", "six": 6}}
#
#
# attrs = {
#     "one": {
#         "type": [{
#             "two": {
#                 "type": int,
#                 "required": False,
#             },
#             "three": {
#                 "type": [int],
#                 "required": True,
#             }
#         }],
#         "required": True,
#     },
#     "four": {
#         "type": {
#             "five": {
#                 "type": int,
#                 "required": True,
#             },
#             "six": {
#                 "type": str,
#                 "required": False,
#             }
#         },
#         "required": True,
#     }
# }

def trans_params(params, attrs):
    # if it is an object
    if isinstance(attrs, dict):
        for k, v in attrs.items():
            obj_type = v["type"]
            required = v["required"]
            if required and params.get(k) is None:
                err_msg = "Missing required key %s" % k
                raise Exception(err_msg)
            if params.get(k) is not None:
                params[k] = trans_params(params[k], obj_type)
    # if it is a list
    elif isinstance(attrs, list):
        if not isinstance(params, list):
            err_msg = "%s is not a list" % params
            raise Exception(err_msg)
        obj_type = attrs[0]
        for ind, _ in enumerate(params):
            params[ind] = trans_params(params[ind], obj_type)
    # if it is a specific type
    else:
        try:
            params = attrs(params)
        except Exception as e:
            err_msg = "param %s trans err, detail %s" % (params, e)
            raise Exception(err_msg)
    return params


# request response utils
def build_response(code, message=None, data=None):
    if message is None:
        message = get_return_message(code)
    return JsonResponse({
        "code": code,
        "message": message,
        "data": data,
    })
