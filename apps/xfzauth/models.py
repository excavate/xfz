from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请输入手机号码！')
        if not username:
            raise ValueError('请输入用户名！')
        if not password:
            raise ValueError('请输入密码！')
        user = self.model(telephone=telephone, username=username, **kwargs)  # 创建用户，用户字段是重新定义后的User中的字段
        user.set_password(password)
        user.save()  # 储存于数据库中,不能遗漏!
        return user

    def create_user(self, telephone, username, password, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 不使用自增长的主键
    # uuid:全球唯一的id。shortuuid 是其较短的版本
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']  # 创建superuser时需要填写的字段,必定含有USERNAME_FIELD和password
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
