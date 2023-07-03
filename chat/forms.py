from django import forms
from .models import *
from django import forms

class PostForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Notification
        fields = ('message', 'read', 'password')




class SearchForm(forms.Form):
    status_choices = (('active', 'Active'), ('terminer', 'Terminer'))
    status = forms.ChoiceField(choices=status_choices)