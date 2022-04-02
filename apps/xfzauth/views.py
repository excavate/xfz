from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse
from utils import restful
from django.shortcuts import redirect, reverse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


@require_POST  # 只能调用post方法
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)  # 如果勾选了记住选项，将session过期时间设为默认的两周
                else:
                    request.session.set_expiry(0)
                return restful.OK()
            else:
                return restful.unauth(message='您的账号已经被封禁了!')
        else:
            return restful.params_errors(message='手机或密码错误!')
    else:
        errors = form.get_errors()
        return restful.params_errors(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        # 需要使用审查过的数据可以使用表单对象.cleaned_data_get提取
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,
                                        username=username, password=password)
        login(request, user)
        return restful.OK()
    else:
        return restful.params_errors(message=form.get_errors())


# 生成图形验证码
def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO相当于一个管道，用来存储图片的流
    out = BytesIO()
    image.save(out, 'png')  # 以png格式，流对象写入image到out中
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从out管道中，读取图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    # 存储验证码到memcached中
    cache.set(text.lower(), text.lower(), 5 * 60)
    return response


# 生成短信验证码
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone, code, 5 * 60)
    print('手机号码是：{0},验证码是：{1}'.format(telephone, code))
    return restful.result(message=code)


def test(request):
    cache.set('name', 'zrm', 60)
    result = cache.get('name')
    print(result)
    return HttpResponse(result)
