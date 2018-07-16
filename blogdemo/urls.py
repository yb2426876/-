"""blogdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",views.login),
    path("logout/",views.logout),
    path("index/",views.index),
    path("",views.index),
    path("updown/",views.updown),
    path("register/",views.register),
    re_path("(?P<username>\w+)/artical/(?P<artical_id>\w+)$",views.artical_detail),
    re_path("(?P<username>\w+)/(?P<condition>category|tag|date)/(?P<params>.*)", views.homesite),
    re_path("(?P<username>\w+)/",views.homesite),
]
