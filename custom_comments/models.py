from django.db import models
from django.contrib.comments.models import Comment
from users.models import Person

class CommentWithVote(Comment):
    votes = models.PositiveIntegerField(default="0")
    voters = models.ManyToManyField(Person)