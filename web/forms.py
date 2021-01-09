from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)

class RecordFilterForm(forms.Form):
    symbol = forms.CharField(label='symbol', max_length=64, required=False)
    start = forms.DateField(label='start', required=False)
    end = forms.DateField(label='end', required=False)