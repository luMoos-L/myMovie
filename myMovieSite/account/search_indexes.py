from haystack import indexes
from .models import movies
class MoviesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):#重载get_model方法
        return movies

    def index_queryset(self, using=None):# 修改return 可以修改返回查询集的内容，比如返回时，有什么条件限制的时候
        return self.get_model().objects.all()
