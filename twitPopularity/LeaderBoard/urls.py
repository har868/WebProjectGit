from django.conf.urls import re_path
from django.urls import include, path
from . import views
from django.contrib.auth.views import login

app_name = 'twitPopularity'

urlpatterns = [
    re_path(r'^$',views.index, name='index'),
    re_path(r'^AddUser/$',views.AddUser,name='AddUser')
    
]