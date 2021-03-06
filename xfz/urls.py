"""xfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.news import views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', include('haystack.urls')),
    path('news/', include('apps.news.urls')),
    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.xfzauth.urls')),
    path('course/', include('apps.course.urls')),
    path('payinfo/', include('apps.payinfo.urls')),
    path('admin/', admin.site.urls),
    path('ueditor/', include('apps.ueditor.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT[0])

