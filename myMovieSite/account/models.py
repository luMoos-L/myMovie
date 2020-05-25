from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class users(models.Model):
    user_name = models.CharField(max_length=10,verbose_name='用户名')
    user_password = models.CharField(max_length=10)
    user_email = models.EmailField(unique=True)
    user_collection = models.CharField(max_length=200)
class EmailRecord(models.Model):
    code = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

class movies(models.Model):
    ch_title = models.CharField(max_length=100)
    en_title = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    pic = models.CharField(max_length=100)
class collections(models.Model):
    user_name = models.CharField(max_length=10,verbose_name='用户名')
    mov_id = models.IntegerField(null=True)
class rate(models.Model):
    user_name = models.CharField(max_length=10, verbose_name='用户名')
    mov_id = models.IntegerField(null=True)
    rate = models.CharField(max_length=50,null=True)

class comments(models.Model):
    movie_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    co_time = models.DateTimeField(auto_now_add=True)
    co_text = models.TextField(default='')