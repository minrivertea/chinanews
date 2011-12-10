from django.db import models
from django.contrib.auth.models import User


from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json


RESERVED_USERNAMES = set((
    # Trailing spaces are essential in these strings, or split() will be buggy
    'feed www help security porn manage smtp fuck pop manager api owner shit '
    'secure ftp discussion blog features test mail email administrator '
    'xmlrpc web xxx pop3 abuse atom complaints news information imap cunt rss '
    'info pr0n about forum admin weblog team feeds root about info news blog '
    'forum features discussion email abuse complaints map skills tags ajax '
    'comet poll polling thereyet filter search zoom machinetags search django '
    'people profiles profile person navigate nav browse manage static css img '
    'javascript js code flags flag country countries region place places '
    'photos owner maps upload geocode geocoding login logout openid openids '
    'recover lost signup reports report flickr upcoming mashups recent irc '
    'group groups bulletin bulletins messages message newsfeed events company '
    'companies active clubs styles style club'
).split())


class Person(models.Model):
    # this is all the core stuff
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField() # we double up the email field so that they can change it if they want
    date_joined = models.DateField()
    
    # now comes all the profile stuff
    karma = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    seen_voting_reminder = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username
        
    def get_latest_posts(self):
        from news.models import NewsItem
        posts = NewsItem.objects.filter(owner=self)[:5]
        return posts


    