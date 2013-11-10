# encoding: utf-8
"""
Profile forms.
"""
from django import forms


class InvitationForm(forms.Form):
    email = forms.EmailField(max_length=128, widget=forms.TextInput(attrs={
        'required': 'true', 'class': 'input', 'placeholder': 'email', 'type': 'email'
    }))


class RegistrationForm(forms.Form):
    name = forms.CharField(label='meno', max_length=64, required=True, widget=forms.TextInput(attrs={
        'required': 'true', 'class': 'input', 'placeholder': 'meno'
    }))
    password1 = forms.CharField(label='heslo', max_length=32, required=True, widget=forms.PasswordInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'heslo'}
    ))
    password2 = forms.CharField(label='zopakuj heslo', max_length=32, required=True, widget=forms.PasswordInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'zopakuj heslo'}
    ))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Heslá sa musia zhodovať.")

        return cleaned_data


class PasswordChangeForm(forms.Form):
    def __init__(self, data=None, user=None):
        self.user = user

        super(PasswordChangeForm, self).__init__(data)

    password = forms.CharField(label='aktuálne heslo', max_length=32, required=True, widget=forms.PasswordInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'aktuálne heslo'}
    ))
    password1 = forms.CharField(label='nové heslo', max_length=32, required=True, widget=forms.PasswordInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'nové heslo'}
    ))
    password2 = forms.CharField(label='zopakuj heslo', max_length=32, required=True, widget=forms.PasswordInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'zopakuj heslo'}
    ))

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()

        if not self.user.check_password(cleaned_data.get('password')):
            raise forms.ValidationError("Nesprávne heslo.")

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Heslá sa musia zhodovať.")

        return cleaned_data


class ProfileUpdateForm(forms.Form):
    name = forms.CharField(label='meno', max_length=64, required=True, widget=forms.TextInput(
        attrs={'required': 'true', 'class': 'input', 'placeholder': 'meno'}
    ))