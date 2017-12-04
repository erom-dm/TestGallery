from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files import File
from urllib.request import urlretrieve
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User)
    vid_bool = models.BooleanField(default=False)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %d %Y')

