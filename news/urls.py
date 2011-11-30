from django.conf.urls.defaults import *

from news.views import *

urlpatterns = patterns('',
    url(r'^$', news_home, name="news_home"),
    url(r'^item/(?P<hashkey>[\w-]+)/blocked$', news_blocked, name="news_blocked"),
    url(r'^item/(?P<hashkey>[\w-]+)/ding$', news_ding, name="news_ding"),
    url(r'^news_ding_ajax$', news_ding_ajax, name="news_ding_ajax"),
    url(r'^item/(?P<hashkey>[\w-]+)$', news_item, name="news_item"),
    url(r'^comment/(?P<id>[\w-]+)/ding$', comment_ding, name="comment_ding"),
    url(r'^add/$', add_news, name="add_news"),
)
