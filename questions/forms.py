from django import forms
 
class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)

    
class AddAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)
    
class SearchForm(forms.Form):
    q = forms.CharField(label='Search')