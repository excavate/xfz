from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from .models import NewsCategory
from utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm, AddBannerForm, EditNewsForm
import os
from django.conf import settings
from apps.news.models import News, Banner
from apps.news.serializer import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


# Create your views here.
# 该装饰器保证了只有公司员工可以使用该视图函数，login_url制定了非公司员工重定向的页面
@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


# 不分页显示所有分类和新闻
# def news_list(request):
#     context = {
#         'categories': NewsCategory.objects.all(),
#         'newses': News.objects.select_related('category', 'author').all()
#     }
#     return render(request, 'cms/news_list.html', context=context)

# 实现分页算法
@method_decorator(permission_required(perm='news.change_news', login_url='/'), name='dispatch')
class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))

        newses = News.objects.select_related('category', 'author')  # select_related查询到的是QuerySet对象

        start = request.GET.get('start')  # 字符串
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')  # 字符串转化成标准时间
            else:
                start_date = datetime(year=2021, month=1, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            newses = newses.filter(title__icontains=title)  # icontains表示大小写不敏感
        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)  # 第一个参数是可迭代对象，2表示每页显示的元素数量
        page_obj = paginator.page(page)  # 获取page对象

        page_info = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,  # 获得包含所有当前页对象的列表
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '',
            })
        }
        context.update(page_info)
        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_mount=2):
        left_has_more = False
        right_has_more = False

        current_page = page_obj.number  # 获取当前页码
        num_pages = paginator.num_pages  # 获取总页数

        if current_page - around_mount >= 3:
            left_has_more = True
            left_pages = range(current_page - around_mount, current_page)
        else:
            left_pages = range(1, current_page)
        if current_page + around_mount < num_pages - 1:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_mount + 1)
        else:
            right_pages = range(current_page + 1, num_pages + 1)
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'current_page': current_page,
            'num_pages': num_pages
        }


@method_decorator(permission_required(perm='news.change_news', login_url='/'), name='dispatch')
class EditNews(View):
    def get(self, request):
        new_id = request.GET.get('news_id')
        news = News.objects.get(id=new_id)
        categories = NewsCategory.objects.all()
        context = {
            'news': news,
            'categories': categories,
        }
        return render(request, 'cms/write_news.html', context)

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get('news_id')
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(id=news_id).update(title=title, desc=desc, thumbnail=thumbnail, content=content)
            return restful.OK()
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm='news.change_news', login_url='/'), name='dispatch')
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {'categories': categories}
        return render(request, 'cms/write_news.html', context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category,
                                author=request.user)
            return restful.OK()
        else:
            return restful.params_errors(message=form.get_errors())


@require_POST
@permission_required(perm='news.delete_news', login_url='/')
def delete_news(request):
    news_id = request.POST.get('news_id')
    try:
        news_rs = News.objects.filter(id=news_id)
        if news_rs.exists():
            thumbnail = news_rs.first().thumbnail
            thumbnail_path = os.path.join(settings.MEDIA_ROOT[0], thumbnail.split('/')[-1])
            try:
                os.remove(thumbnail_path)
                return restful.OK()
            except OSError:
                return restful.params_errors(message='不能删除目录！')
            except:
                return restful.params_errors(message='删除文件失败')
            finally:
                news_rs.delete()
    except Exception as e:
        return restful.params_errors(message=e)


@require_GET
@permission_required(perm='news.add_newscategory', login_url='/')
def news_category(request):
    categories = NewsCategory.objects.all()
    categories_num = len(categories)
    context = {'categories': categories, 'categories_num': categories_num}
    return render(request, 'cms/news_category.html', context=context)


@require_POST
@permission_required(perm='news.add_newscategory', login_url='/')
def add_news_category(request):
    name = request.POST.get('name')
    exist = NewsCategory.objects.filter(name=name).exists()
    if not exist:
        NewsCategory.objects.create(name=name)
        return restful.OK()
    else:
        return restful.params_errors(message='该分类已存在！')


@require_POST
@permission_required(perm='news.change_newscategory', login_url='/')
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(id=pk).update(name=name)  # id和pk是一样的,都是指主键，其他不是
            return restful.OK()
        except:
            return restful.params_errors(message='该分类不存在！')
    else:
        errors = form.get_errors()
        return restful.params_errors(message=errors)


@require_POST
@permission_required(perm='news.delete_newscategory', login_url='/')
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.OK()
    except:
        return restful.unauth(message='该分类不存在！')


@require_POST
@staff_member_required(login_url='/')
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    if os.path.exists(os.path.join(settings.MEDIA_ROOT[0], name)):
        return restful.params_errors(message='该文件已存在！请修改文件名重新上传！')
    with open(os.path.join(settings.MEDIA_ROOT[0], name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)  # 该方法已写好了网站所在的地址和端口（现在是localhost:8000）
    # 参数即需要补充的文件相对路径
    return restful.result(data={'url': url})


@permission_required(perm='news.add_banner', login_url='/')
def banners(request):
    return render(request, 'cms/banners.html')


@permission_required(perm='news.add_banner', login_url='/')
def banner_list(request):
    banner_query = Banner.objects.all()  # 返回的是query对象，故需要使many=True
    serilize = BannerSerializer(banner_query, many=True)
    print("序列化后的banner：", serilize.data)
    return restful.result(data=serilize.data)


@permission_required(perm='news.add_banner', login_url='/')
def add_banners(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_errors(message=form.get_errors())


@permission_required(perm='news.change_banner', login_url='/')
def edit_banner(request):
    banner_id = request.POST.get('pk')
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.filter(pk=banner_id).update(priority=priority, image_url=image_url, link_to=link_to)
        return restful.result(data={'banner_id': banner_id})
    else:
        return restful.params_errors(message=form.get_errors())


@permission_required(perm='news.delete_banner', login_url='/')
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    try:
        Banner.objects.filter(pk=banner_id).delete()
        return restful.OK()
    except:
        return restful.unauth(message="该缩略图不存在！")
