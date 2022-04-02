from rest_framework import serializers
from .models import News, Comment, Banner
from apps.cms.models import NewsCategory
from apps.xfzauth.serializer import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


# 序列化重新定义了要显示的条目，model指定要序列化的模型，fields指定要序列化的条目，可以像下面一样嵌套序列化。
class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'author', 'pub_time', 'category')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'priority', 'link_to')
