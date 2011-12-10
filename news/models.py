from django.db import models
from urlparse import urlparse
from django.core.urlresolvers import reverse

from users.models import Person


class NewsItem(models.Model):
    owner = models.ForeignKey(Person)
    date = models.DateTimeField()
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    votes = models.PositiveIntegerField(default="0")
    hashkey = models.CharField(max_length=256)
    voters = models.ManyToManyField(Person, db_index=True, related_name="Voters", null=True, blank=True)
    blocked = models.PositiveIntegerField(default="0")
    
    def __unicode__(self):
        return self.title
        
    def is_blocked(self):
        blocked = False
        if self.blocked > 3:
            blocked = True
        
        return blocked
    
    def show_url(self):
        url = urlparse(self.url)
        return url.netloc
   
    def get_comment_count(self):
        from custom_comments.models import CommentWithVote
        count = CommentWithVote.objects.filter(object_pk=self.pk).count()
        return count
    
    def get_absolute_url(self):
        url = reverse('news_item', args=[self.hashkey])
        return url
    
    class Meta:
        ordering = ['-date']