from django.views import View
from .consts import ReturnCode
from .utils import build_response
from user.handler import UserHandler
from user.consts import USER_TOKEN_COOKIE_NAME


class BaseView(View):
    def __init__(self):
        super(BaseView, self).__init__()
        self._need_login = False  # check whether user should log in, if permission handler is set, it will be True
        self._permission_handler = None  # check the user's permission, should be a function
        self.current_user = None  # the current user instance

    def dispatch(self, request, *args, **kwargs):
        # first get the current user
        if self._permission_handler is not None or self._need_login is True:
            user_handler = UserHandler()
            user_token_str = request.COOKIES.get(USER_TOKEN_COOKIE_NAME)
            if user_token_str is not None: 
                self.current_user = user_handler.get_current_user_from_token_str(user_token_str)
            else:
                self.current_user = None
            if self.current_user is None:
                return_code = ReturnCode.NotLogIn
                resp = build_response(return_code)
                return resp
        if self._permission_handler is not None:
            # in the current version we don't implement this
            pass
        return super(BaseView, self).dispatch(request, *args, **kwargs)
