from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('cms.NewsCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('xfzauth.User', on_delete=models.SET_NULL, null=True)

    # 按时间倒序排序
    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='comments')
    # 级联删除，即新闻被删除，它关联的评论也会被删除;related_name是通过news访问所有评论时，可通过comments访问
    author = models.ForeignKey('xfzauth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']


class Banner(models.Model):
    priority = models.IntegerField(default=0)
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']

