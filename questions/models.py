from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

from users.models import Person


class QuestionManager(models.Manager):
    def filter(self):
        qs = super(QuestionManager, self).get_query_set()
        return qs.filter()

class Question(models.Model):
    date = models.DateTimeField()
    owner = models.ForeignKey(Person)
    question = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200)
    votes = models.IntegerField(default="0")
    voters = models.ManyToManyField(Person, related_name="question_voters")
    is_published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.question     

    def get_absolute_url(self):
        return "/questions/%s/" % self.slug
    
    def answers_count(self):
        answers = Answer.objects.filter(question=self)
        return answers.count() 
    
        
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='to_question')
    owner = models.ForeignKey(Person)
    answer = models.TextField()
    date_added = models.DateTimeField(default=datetime.now())
    votes = models.IntegerField(default="0")
    voters = models.ManyToManyField(Person, related_name="answer_voters")
    is_published = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s, %s" % (self.owner, self.answer)      
