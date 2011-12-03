from django import forms


class InviteUserForm(forms.Form):
    email = forms.CharField(required=True)
    
    
class CompleteUserDetailsForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)