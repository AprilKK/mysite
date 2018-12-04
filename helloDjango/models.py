# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.
class Artical(models.Model):
    articalId = models.AutoField(primary_key = True) # auto incremental for the primary key.
    #you use primary_key = True if you do not want to use default field "id" given by django to your model
    title = models.CharField(max_length = 100)
    subtitle = models.CharField(max_length = 500)
    content = models.TextField()
    submittedDate = models.DateField(default = date.today)
    lastUpdatedDate = models.DateField(default = date.today)
    author = models.CharField(default = 'xikong', max_length = 50)

# use __str__ for python 3
def __unicode__(self):
    return self.title

class Comment(models.Model):
    commentId = models.AutoField(primary_key = True)
    articalId = models.ForeignKey(Artical)
    comment = models.TextField()
    commentDate = models.DateField(default = date.today)
    author = models.CharField(max_length = 50)

# use __str__ for python 3
def __unicode__(self):
    return self.comment[:10]

