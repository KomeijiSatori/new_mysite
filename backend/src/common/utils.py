import time
import django_redis


def get_redis_connection():
    conn = django_redis.get_redis_connection("default")
    return conn

def get_current_timestamp():
    return int(time.time())

def redis_hget(key, field):
    conn = get_redis_connection()
    return conn.hget(key, field)

def redis_hset(key, field, value):
    conn = get_redis_connection()
    conn.hset(key, field, value)


