from django.shortcuts import render, redirect, reverse
from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator
from django.contrib import messages


@xfz_superuser_required
def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs': staffs
    }
    return render(request, 'cms/staff.html', context=context)


@method_decorator(xfz_superuser_required, name='dispatch')  # 给类视图添加装饰器，get和post最终都会调用dispatch方法
class AddStaffView(View):
    def post(self, request):
        telephone = request.POST.get('telephone')
        groups_ids = request.POST.getlist('groups')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            groups = Group.objects.filter(id__in=groups_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            messages.info(request, '用户不存在！')
            return redirect(reverse('cms:add_staffs'))

    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'cms/add_staffs.html', context={'groups': groups})
