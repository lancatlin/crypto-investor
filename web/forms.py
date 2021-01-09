from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)

class DateInput(forms.DateInput):
    input_type = 'date'


class RecordFilterForm(forms.Form):
    symbol = forms.CharField(label='symbol', max_length=64, required=False)
    start = forms.DateField(label='start', required=False, widget=DateInput)
    end = forms.DateField(label='end', required=False, widget=DateInput)