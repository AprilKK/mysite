# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import staticfiles 
from helloDjango.models import Artical
import markdown
from .forms import UploadFileForm
from helloDjango.tools.fileTools import handle_upload_file

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

def uploadFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_upload_file(request.FILES.get('file',None))
            art = Artical()
            art.title = form.cleaned_data['ArticalTitle']
            art.subtitle = form.cleaned_data['ArticalSubtitle']
            art.content = form.cleaned_data['ArticalAbstract']
            art.fileName = form.name
            art.save()
            return HttpResponse('file uploaded sucessfully...')
    else:
        form = UploadFileForm()

    return render(request,'uploadFile.html',{'form':form})