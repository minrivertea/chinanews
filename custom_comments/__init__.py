from custom_comments.models import CommentWithVote
from custom_comments.forms import CommentFormWithVote

def get_model():
    return CommentWithVote

def get_form():
    return CommentFormWithVote