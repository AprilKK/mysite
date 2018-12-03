# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import staticfiles 
def index(request):
    return render(request,'index.html')

def stable(request):
    return render(request,'home.html')
