from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpRequest, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .binance_client import Binance
from .models import User, Record

# Create your views here.

def index(request: HttpRequest):
    return render(request, 'index.html')

@login_required
def reload_orders(request: HttpRequest):
    return StreamingHttpResponse(load_orders(request.user))

def load_orders(user: User):
    client = Binance(user) 
    for record, created in client.records():
        if not created:
            record.save()
            yield f"{record.time}\n"

def login(request):
    if request.method != 'POST':
        return render(request, 'login.html', {'msg': '', 'form': LoginForm()})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'msg': 'Form Not Falid', 'form': LoginForm()})

    user = auth.authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is None:
        return render(request, 'login.html', {'msg': '驗證失敗', 'form': LoginForm()})

    auth.login(request, user)
    return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def records_list(request: HttpRequest):
    user = request.user
    return render(request, 'records.html', {'records': Record.objects.all().filter(user=user)})