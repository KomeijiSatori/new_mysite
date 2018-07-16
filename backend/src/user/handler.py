from django.conf import settings
from .utils import generate_token
from common.utils import redis_hget, redis_hset, get_current_timestamp, get_timestamp_from_now
from .service import UserService


class UserHandler(object):
    def __init__(self):
        self.user_service = UserService()

    def _check_user_login(self, user_id, user_token):
        """
        Check the user with user_id to be login according to the token
        :param user_id: int
        :param user_token: dict
        :return: bool
        """
        # check the valid token
        redis_token, expire_time = self.user_service.get_login_info_from_redis(user_id)
        if redis_token is None or expire_time is None:
            return False
        if redis_token != user_token:
            return False
        current_timestamp = get_current_timestamp()
        if current_timestamp > expire_time:
            return False
        return True

    def get_current_user_from_token_str(self, user_token_str):
        """
        Get the current user from the request
        :param request: HttpRequest, the request
        :return: User, the user
        """
        user_id, user_token = self.user_service.get_login_info_from_jwt_token(user_token_str)
        if user_id is None or user_token is None:
            return None
        if self._check_user_login(user_id, user_token):
            user = self.user_service.get_user_by_id(user_id)
            return user
        else:
            return None

    def get_token_str_for_current_user(self, user_id):
        """
        Set the user token after login
        :param user_id: int
        :return: token: str
        """
        expire_days = settings.LOGIN_TOKEN_EXPIRE_DAYS
        login_token = generate_token()
        expire_time = get_timestamp_from_now(days=expire_days)
        # save the login info to redis
        self.user_service.set_login_info_to_redis(user_id, login_token, expire_time)
        # return the token to client
        user_token_str = self.user_service.get_jwt_token_from_login_info(user_id, login_token)
        return user_token_str
