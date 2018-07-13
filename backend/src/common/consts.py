class ReturnCode(object):
    Success = 0
    # login related
    NotLogIn = 10000
    NoPermission = 10001


MessageMap = {
    ReturnCode.Success: "",
    ReturnCode.NotLogIn: "Not Login",
    ReturnCode.NoPermission: "Permission Denied",
}

def get_return_message(return_code):
    return MessageMap.get(return_code)
