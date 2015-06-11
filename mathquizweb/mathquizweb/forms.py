from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class QuestionForm(forms.Form):
    answer = forms.CharField(label='Answer')
    uuid = forms.CharField(label='uuid', widget=forms.widgets.HiddenInput)
