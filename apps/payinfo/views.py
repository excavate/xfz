from django.shortcuts import render
from .models import PayInfo
import os
from django.conf import settings
from django.http import FileResponse, Http404


def index(request):
    payinfos = PayInfo.objects.all()
    context = {
        'payinfos': payinfos,
    }
    return render(request, 'payinfo/payinfo.html', context=context)


def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = PayInfo.objects.filter(pk=payinfo_id).first()
    if payinfo:
        path = payinfo.path
        fp = open(os.path.join(settings.MEDIA_ROOT[0], path), 'rb')
        response = FileResponse(fp)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment;filename="%s"' % path.split('/')[-1]  # 以附件的形式下载，同时指定文件名称
        return response
    else:
        return Http404()
