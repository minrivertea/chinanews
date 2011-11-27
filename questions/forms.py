from django import forms
 
class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200, label="* Question title")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Extra information/details")

    
class AddAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)
    
class SearchForm(forms.Form):
    q = forms.CharField(label='Search')