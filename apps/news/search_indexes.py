from haystack import indexes
from .models import News

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # 指定需要建立索引的模型
    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()