from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from news.models import *


class AddNewsForm(forms.Form):
    title = forms.CharField(required=True, label='* Title')
    url = forms.CharField(required=False, label='URL', 
        help_text="Use this if you're posting a link")
    text = forms.CharField(widget=forms.Textarea, required=False, label='Text',
        help_text="Use this if you're starting a discussion")