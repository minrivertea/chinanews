from django import forms
from django.contrib.comments.forms import CommentForm
from custom_comments.models import CommentWithVote
from users.models import Person

class CommentFormWithVote(CommentForm):
    votes = forms.IntegerField(required=False)

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentWithVote

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormWithVote, self).get_comment_create_data()
        data['votes'] = self.cleaned_data['votes']
        return data