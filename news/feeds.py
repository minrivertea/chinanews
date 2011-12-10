from django.contrib.syndication.feeds import Feed
from news.models import NewsItem
from news.views import _get_news

class LatestEntries(Feed):
    title = "News from wheninchina.com"
    link = "/"
    description = "Top 20 news stories from around China today."

    def items(self, request):
        return _get_news(request)

    def item_description(self, item):
        return item.url
        
    def item_title(self, item):
        return item.title



