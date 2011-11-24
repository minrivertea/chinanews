from django.db import models
from django.contrib.auth.models import User


from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json



class Person(models.Model):
    # this is all the core stuff
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField() # we double up the email field so that they can change it if they want
    date_joined = models.DateField()
    
    # now comes all the profile stuff
    karma = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField()
    
    def __unicode__(self):
        return self.user.username
        
    def get_latest_posts(self):
        from news.models import NewsItem
        posts = NewsItem.objects.filter(owner=self)[:5]
        return posts


    