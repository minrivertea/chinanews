from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
import re
from urlparse import urlparse, urljoin

from users.models import Person
from news.models import *



class AddNewsForm(forms.Form):
    title = forms.CharField(required=True, label='* Title')
    url = forms.CharField(required=False, label='URL', 
        help_text="Use this if you're posting a link")
    text = forms.CharField(widget=forms.Textarea, required=False, label='Text',
        help_text="Use this if you're starting a discussion")
    as_user = forms.ModelChoiceField(required=False, queryset=Person.objects.filter(user__is_staff=True), 
        label="As user")
    
    
    def clean_url(self):
        # we just want to check that the URL is properly formed
        url = self.cleaned_data['url']
        data = urlparse(url)
        if not data.scheme:
            url = "http://%s" % url
                
        return url


