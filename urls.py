from django.conf.urls.defaults import *
import django.views.static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from news.views import index
from news.feeds import LatestEntries
from users.views import *
from custom_comments.views import comment_reply

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    url(r'^$', index, name="home"),
    url(r'^invite_user/$', invite_user, name="invite_user"),
    url(r'^seen_voting_reminder/$', seen_voting_reminder, name="seen_voting_reminder"),
    url(r'^invite/(?P<key>[\w-]+)$', activate_invited_user, name="activate_invited_user"),
    url(r'^profile/edit_bio$', edit_bio, name="edit_bio"),
    url(r'^profile/$', user_profile, name="user_profile"),
    url(r'^profile/(?P<slug>[\w-]+)/all_posts$', all_posts, name="all_posts"),
    url(r'^profile/(?P<slug>[\w-]+)$', profile, name="profile"),
    url(r'^comment/reply/(?P<hashkey>[\w-]+)/(?P<id>[\w-]+)$', comment_reply, name="comment_reply"),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="latest_feed"),
    (r'^news/', include('news.urls')),
    (r'^questions/', include('questions.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
)


# for the development server static files
urlpatterns += patterns('',

    # CSS, Javascript and IMages
    (r'^photos/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/photos',
        'show_indexes': settings.DEBUG}),
    (r'^images/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/images',
        'show_indexes': settings.DEBUG}),
    (r'^cache/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/cache',
        'show_indexes': settings.DEBUG}),
    (r'^thumbs/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/thumbs',
        'show_indexes': settings.DEBUG}),
    (r'^css/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/css',
        'show_indexes': settings.DEBUG}),
    (r'^js/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/js',
        'show_indexes': settings.DEBUG}),
)