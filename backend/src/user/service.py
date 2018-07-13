import pickle
from django.contrib.auth.models import User

from common.utils import redis_hget, redis_hset
from .consts import USER_CACHE_HSET_NAME


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
        self._set_user_to_cache(user)
        return user
