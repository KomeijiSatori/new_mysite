import json

from .utils import jwt_decode
from common.utils import get_redis_connection, get_current_timestamp
from .consts import USER_TOKEN_COOKIE_NAME, USER_TOKEN_USER_ID_NAME, USER_TOKEN_VALID_TOKEN_NAME, \
    USER_TOKEN_HSET_NAME, REDIS_TOKEN_VALID_TOKEN_NAME, REDIS_TOKEN_EXPIRE_TIME_NAME
from .service import UserService


class UserHandler(object):
    def check_user_login(self, user_id, user_token):
        """
        Check the user with user_id to be login according to the token
        :param user_id: int
        :param user_token: dict
        :return: bool
        """
        # check the valid token
        conn = get_redis_connection()
        redis_token_info_byte = conn.hget(USER_TOKEN_HSET_NAME, user_id)
        try:
            redis_token_info_str = bytes.decode(redis_token_info_byte)
            redis_token_info = json.loads(redis_token_info_str)
            redis_token = redis_token_info[REDIS_TOKEN_VALID_TOKEN_NAME]
            expire_time = redis_token_info[REDIS_TOKEN_EXPIRE_TIME_NAME]
            if redis_token != user_token:
                return False
            current_timestamp = get_current_timestamp()
            if current_timestamp > float(expire_time):
                return False
            return True
        except Exception:
            return False


    def get_current_user_from_request(self, request):
        """
        Get the current user from the request
        :param request: HttpRequest, the request
        :return: User, the user
        """
        user_token_str = request.COOKIES.get(USER_TOKEN_COOKIE_NAME)
        if not user_token_str:
            return None
        user_token_info = jwt_decode(user_token_str)
        if user_token_info is None:
            return None
        user_id = user_token_info.get(USER_TOKEN_USER_ID_NAME)
        user_token = user_token_info.get(USER_TOKEN_VALID_TOKEN_NAME)
        if self.check_user_login(user_id, user_token):
            try:
                user_service = UserService()
                user = user_service.get_user_by_id(user_id)
                return user
            except Exception:
                return None
        else:
            return None
