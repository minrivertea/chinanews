from django.db import models

from users.models import Person


class NewsItem(models.Model):
    owner = models.ForeignKey(Person)
    date = models.DateTimeField()
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    votes = models.PositiveIntegerField(default="0")
    hashkey = models.CharField(max_length=256)
    voters = models.ManyToManyField(Person, db_index=True, related_name="Voters")
    
    def __unicode__(self):
        return self.title