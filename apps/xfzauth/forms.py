from django import forms
from apps.forms import FormMixin
from .models import User
from django.core.cache import cache


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码不能超过20位!',
                                               'min_length': '密码不能少于6位!'})
    remember = forms.IntegerField(required=False)  # 浏览器不会记住该表单


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6,
                                error_messages={'max_length': '密码不能超过20位!',
                                                'min_length': '密码不能少于6位!'})
    password2 = forms.CharField(max_length=20, min_length=6,
                                error_messages={'max_length': '密码不能超过20位!',
                                                'min_length': '密码不能少于6位!'})
    img_captcha = forms.CharField(min_length=4, max_length=4)
    sms_captcha = forms.CharField(min_length=4, max_length=4)

    def clean(self):
        # clean方法对表单中的数据进行审查，可通过重写clean自定义之
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次输入密码不一致！')

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError('图形验证码错误！')
        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)
        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')
        # 通过filter查询需要的条目，用.exists判断其是否存在
        exits = User.objects.filter(telephone=telephone).exists()
        if exits:
            raise forms.ValidationError('该手机号码已被注册！')
