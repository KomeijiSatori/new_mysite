from django.views import View
from django.http import JsonResponse
from .consts import ReturnCode, get_return_message
from user.handler import UserHandler


class BaseView(View):
    def __init__(self):
        super(BaseView, self).__init__()
        self._need_login = False  # check whether user should log in, if permission handler is set, it will be True
        self._permission_handler = None  # check the user's permission, should be a function
        self.current_user = None  # the current user instance

    def dispatch(self, request, *args, **kwargs):
        # first get the current user
        if self._permission_handler is not None or self._need_login is not None:
            user_handler = UserHandler()
            self.current_user = user_handler.get_current_user_from_request(request)
            if self.current_user is None:
                return_code = ReturnCode.NotLogIn
                resp = {'code': return_code, 'message': get_return_message(return_code)}
                return JsonResponse(resp)
        if self._permission_handler is not None:
            # in the current version we don't implement this
            pass
        return super(BaseView, self).dispatch(request, *args, **kwargs)
