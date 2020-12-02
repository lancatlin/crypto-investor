from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'records.html')

def reload_orders(request):
    pass 

def login_form(request):
    if request.method != 'POST':
        return render(request, 'login.html', {'msg': '', 'form': LoginForm()})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'msg': 'Form Not Falid', 'form': LoginForm()})

    user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is None:
        return render(request, 'login.html', {'msg': '驗證失敗', 'form': LoginForm()})

    login(request, user)
    return HttpResponseRedirect('/')