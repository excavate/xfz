from django.db import models
from shortuuidfield import ShortUUIDField


class PayInfo(models.Model):
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    path = models.FilePathField()



