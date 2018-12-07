# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import staticfiles 
from helloDjango.models import Artical
import markdown
def index(request):
    return render(request,'index.html')

def stable(request):
    return render(request,'home.html')

def blog(request):
    currentPage = 1
    page = request.GET.get('page')
    if page is not None:
        page = int(page)
    else:
        page = 1
    if -1 == page:
       currentPage = currentPage +1 
    else:
        currentPage = page
    artlist = Artical.objects.all()[(currentPage-1)*3:currentPage*3]
    return render(request,'blog.html',{'artlist':artlist})

def artical(request):
    artId = request.GET.get('id')
    if artId is not None:
        artId = int(artId)
    else:
        artId = 0
    art = Artical.objects.get(articalId = artId)
    if art is None:
        return HttpResponse('no artical')
    artFileName = art.fileName
    with open('./helloDjango/articals/'+artFileName) as f:
        content = f.read()
    contentutf = unicode(content,'utf-8')
    art = markdown.markdown(contentutf,extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    return render(request,'artical.html',{'content':art})