from utils import restful
from django.shortcuts import redirect
from functools import wraps
from django.http import Http404


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message="用户未登录！")
            else:
                return redirect('/')

    return wrapper


def xfz_superuser_required(func):
    @wraps(func)  # 不改变原来函数__name__等内置函数的值
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise Http404

    return decorator
