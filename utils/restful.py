from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def result(code=HttpCode.ok, message='', data=None, kwargs=None):  #kwargs接收别的参数
    jason_dict = {'code': code, 'message': message, 'data': data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        jason_dict.update(kwargs)
    return JsonResponse(jason_dict)


def OK(message='', data=None):
    return result()


def params_errors(message='', data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message='', data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_errors(message='', data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_errors(message='', data=None):
    return result(code=HttpCode.servererror, message=message, data=data)
