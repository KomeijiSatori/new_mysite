import pickle
import json
from django.contrib.auth.models import User

from common.utils import redis_hget, redis_hset
from .utils import jwt_decode, jwt_encode
from .consts import USER_CACHE_HSET_NAME, USER_TOKEN_USER_ID_NAME, USER_TOKEN_VALID_TOKEN_NAME, \
    USER_TOKEN_HSET_NAME, REDIS_TOKEN_VALID_TOKEN_NAME, REDIS_TOKEN_EXPIRE_TIME_NAME


class UserService(object):
    def _get_user_from_cache(self, user_id):
        key = USER_CACHE_HSET_NAME
        field = user_id
        data = redis_hget(key, field)
        # if hit cache
        if data is not None:
            user = pickle.loads(data)
            return user
        return None

    def _get_user_from_db(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            return None
        return user

    def _set_user_to_cache(self, user):
        if user is None:
            return
        key = USER_CACHE_HSET_NAME
        field = user.id
        data = pickle.dumps(user)
        redis_hset(key, field, data)

    def get_user_by_id(self, user_id):
        """
        Get a user instance by user_id
        :param user_id: int
        :return: User
        """
        # first refer to cache
        user = self._get_user_from_cache(user_id)
        if user is not None:
            return user
        # then refer to db
        user = self._get_user_from_db(user_id)
        # then save to cache
        if user is not None:
            self._set_user_to_cache(user)
        return user

    def get_login_info_from_redis(self, user_id):
        """
        Get a user's login info from redis
        :param user_id: int
        :return: {token, expire_time}
        """
        redis_token_info_byte = redis_hget(USER_TOKEN_HSET_NAME, user_id)
        try:
            redis_token_info_str = bytes.decode(redis_token_info_byte)
            redis_token_info = json.loads(redis_token_info_str)
            redis_token = redis_token_info[REDIS_TOKEN_VALID_TOKEN_NAME]
            expire_time = redis_token_info[REDIS_TOKEN_EXPIRE_TIME_NAME]
            return redis_token, expire_time
        except Exception:
            return None, None

    def get_login_info_from_jwt_token(self, user_token_str):
        """
        Decode jwt token from user_token_str
        :param user_token_str: str
        :return: {user_id, user_token}
        """
        user_token_info = jwt_decode(user_token_str)
        if user_token_info is None:
            return None, None
        user_id = user_token_info.get(USER_TOKEN_USER_ID_NAME)
        user_token = user_token_info.get(USER_TOKEN_VALID_TOKEN_NAME)
        return user_id, user_token

    def set_login_info_to_redis(self, user_id, token, expire_time):
        """
        Save token to redis
        :param user_id: int
        :param token: str
        :param expire_time: float
        :return: 
        """
        redis_token_info = {}
        redis_token_info[REDIS_TOKEN_VALID_TOKEN_NAME] = token
        redis_token_info[REDIS_TOKEN_EXPIRE_TIME_NAME] = expire_time
        redis_token_info_str = json.dumps(redis_token_info)
        redis_hset(USER_TOKEN_HSET_NAME, user_id, redis_token_info_str)

    def get_jwt_token_from_login_info(self, user_id, user_token):
        """
        Encode jwt token from login info
        :param user_id: int
        :param user_token: str
        :param expire_time: float
        :return: 
        """
        user_token_info = {}
        user_token_info[USER_TOKEN_USER_ID_NAME] = user_id
        user_token_info[USER_TOKEN_VALID_TOKEN_NAME] = user_token
        user_token_str = jwt_encode(user_token_info)
        return user_token_str

