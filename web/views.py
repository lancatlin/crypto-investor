from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpRequest, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import LoginForm, RecordFilterForm
from .binance_client import Binance
from .models import User, Record, calculate_profit
from datetime import datetime, timezone, timedelta

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
        yield f"{record.time}<br>"

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

class RecordList(generic.ListView):
    model = Record
    #paginate_by = 10
    
    def get_queryset(self):
        tx = Record.objects.filter(user=self.request.user).order_by('-time')
        form = RecordFilterForm(self.request.GET or None)
        if form.is_valid() :
            form = form.cleaned_data
            print(form)
            if form['symbol'] != '':
                tx = tx.filter(symbol__contains=form['symbol'])
            if form['start'] is not None:
                tx = tx.filter(time__gt=form['start'])
            if form['end'] is not None:
                tx = tx.filter(time__lt=form['end'] + timedelta(days=1))

        return tx
    
    def get_context_data(self, **kwargs):
        ctx = super(RecordList, self).get_context_data(**kwargs)
        ctx['profit'] = calculate_profit(self.get_queryset().all(), Binance(self.request.user).price)
        ctx['form'] = RecordFilterForm(self.request.GET or None)
        return ctx
