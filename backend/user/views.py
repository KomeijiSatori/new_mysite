import logging
from django.contrib.auth import authenticate
from django.conf import settings

from .handler import UserHandler
from .consts import USER_TOKEN_COOKIE_NAME
from common.base_view import BaseView
from common.consts import ReturnCode
from common.utils import get_params, post_params, trans_params, build_response

# Create your views here.

class LoginView(BaseView):
    def __init__(self):
        super(LoginView, self).__init__()
        self.http_method_names = ['post']
        self.attrs = {
            "user_name": {
                "type": str,
                "required": True,
            },
            "user_password": {
                "type": str,
                "required": True,
            }
        }

    def get_clean_params(self, request):
        try:
            params = post_params(request)
            clean_params = trans_params(params, self.attrs)
        except Exception as e:
            logging.error(e)
            return None, e
        return clean_params, None

    def post(self, request, *args, **kwargs):
        params, err = self.get_clean_params(request)
        if err is not None:
            resp = build_response(ReturnCode.ParamError, message=str(err))
            return resp
        name = params.get("user_name")
        password = params.get("user_password")
        user = authenticate(username=name, password=password)
        if user is not None:
            handler = UserHandler()
            user_id = user.id
            token = handler.get_token_str_for_current_user(user_id)
            # return response
            code = ReturnCode.Success
            message = "Login Success"
            data = {"user_name": user.username, "user_id": user.id}
            resp = build_response(code, message=message, data=data)
            # set cookie
            max_age = settings.LOGIN_TOKEN_EXPIRE_DAYS * 86400
            resp.set_cookie(USER_TOKEN_COOKIE_NAME, token, max_age=max_age)
            return resp
        else:
            # the user fail the authentication
            code = ReturnCode.AuthenticationFail
            resp = build_response(code)
            return resp


class LogoutView(BaseView):
    def __init__(self):
        super(LogoutView, self).__init__()
        self._need_login = True
        self.http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        handler = UserHandler()
        user_id = self.current_user.id
        handler.remove_token_for_current_user(user_id)
        # return response
        code = ReturnCode.Success
        message = "Logout Success"
        resp = build_response(code, message=message)
        # set cookie
        resp.set_cookie(USER_TOKEN_COOKIE_NAME, '')
        return resp


class UserInfoView(BaseView):
    def __init__(self):
        super(UserInfoView, self).__init__()
        self._need_login = True
        self.http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        data = {
            "user_name": self.current_user.username,
            "user_id": self.current_user.id,
        }
        code = ReturnCode.Success
        resp = build_response(code, data=data)
        return resp
