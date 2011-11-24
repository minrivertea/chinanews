from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from news.models import *


class AddNewsForm(forms.Form):
    url = forms.CharField(required=False)
    title = forms.CharField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=False)