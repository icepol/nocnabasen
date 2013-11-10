"""
TODO: what is this?
"""
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=200)