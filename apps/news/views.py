from django.shortcuts import render
from apps.news.models import News, Banner
from apps.cms.models import NewsCategory
from django.conf import settings
from .serializer import NewsSerializer, CommentSerializer
from utils import restful
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('author', 'category').all()[:count]  # select_related可将关联的外键和本来的模型都查出来
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {'newses': newses, 'categories': categories, 'banners': banners}
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过url里的p参数指定要获取的数据，1是p没有赋值时给page的默认值
    page = int(request.GET.get('p', 1))
    # 分类为0表示不进行任何分类，直接按照倒序排序
    category = int(request.GET.get('category_id', 0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = page * settings.ONE_PAGE_NEWS_COUNT

    if category == 0:
        newses = News.objects.select_related('category', 'author').all()[start:end]  # 返回query对象，故下方还需声明many=True
    else:
        newses = News.objects.select_related('category', 'author').filter(category__id=category)[start:end]

    # 序列化将QuerySet对象的值变成序列化中预设的信息
    # {'id':1,'title':abc,'category':{'id':1,'name':a}}
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related('comments__author').get(pk=news_id)
        # prefetch_related查询外键所有关联的条目（“我称之为源键”）
        context = {'news': news}
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        author = request.user
        comment = Comment.objects.create(news_id=news_id, content=content, author=author)  # 返回comment对象
        serializecomment = CommentSerializer(comment)
        return restful.result(data=serializecomment.data)
    else:
        return restful.params_errors(message=form.get_errors())


def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newes = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        context['newes'] = newes
    return render(request, 'search/search1.html', context=context)
