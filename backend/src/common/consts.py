class ReturnCode(object):
    Success = 0
    # login related
    NotLogIn = 10000
    NoPermission = 10001
    AuthenticationFail = 10002
    # common error
    ParamError = 20000


MessageMap = {
    ReturnCode.Success: "Success",
    ReturnCode.NotLogIn: "Not Login",
    ReturnCode.NoPermission: "Permission Denied",
    ReturnCode.AuthenticationFail: "Authenticate Failed",
    ReturnCode.ParamError: "Parameter Error",
}

def get_return_message(return_code):
    return MessageMap.get(return_code)
