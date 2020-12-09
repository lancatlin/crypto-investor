from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from web.views import index, login, logout, reload_orders, RecordList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login', login),
    path('logout', logout),
    path('reload', reload_orders),
    path('records', login_required(RecordList.as_view())),
]
