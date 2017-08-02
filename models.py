from __future__ import unicode_literals
from django.db import models
from listfield import ListField,CompressedTextField
# Create your models here.
class Mysite(models.Model):
	title = models.CharField(max_length=100)
	url = models.URLField()
	author = models.CharField(max_length=100)
	num = models.IntegerField(max_length=10)
	def __unicode__(self):
		return self.title	
class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	def __unicode__(self):
		return self.title
'''class BBS(models.Model):
	title = models.CharField(max_length = 64)
	summary = models.CharField(max_length = 256,blank = True)
	content = models.TextFeild()
	author = models.ForeignKey('Users')
	view_count = models.IntegerField()
	ranking = models.IntegerField()
	created_at = models.DateTimeField()
	update_at = models.DateTimeField()
	def __unicode__(self):
		return self.title'''
'''class Category(models.Model):
	name = models.CharField(max_length = 32,unique = True)'''
class BBS(models.Model):
	title = models.CharField(max_length = 64)
	summary = models.CharField(max_length = 256 , blank = True)
	content = models.TextField(max_length=1000)
	author = models.CharField(max_length = 50)
	view_count = models.IntegerField(default=1)
	ranking = models.IntegerField(default=100)
	rank_id = models.IntegerField(default = 1)
	comment_others = models.CharField(max_length = 10000,default = "")
	def __unicode__(self):
		return self.title
class BBS_hupu_tianya(models.Model):
	title = models.CharField(max_length = 100)
	time = models.CharField(max_length = 20)
	reply = models.CharField(max_length = 10)
	go_through = models.CharField(max_length = 10)
	url = models.CharField(max_length = 100)
class Picture_search(models.Model):
	photo = models.ImageField(upload_to = "search_file",default="/static/img/target.jpg")
class BBS_users(models.Model):
	#user = models.OneToOneField(Users)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	signature = models.CharField(max_length=128,default='this gay is too lazy to leave anything here',editable=False)
	photo = models.ImageField(upload_to = "up_img",default = "/static/img/1.jpg")
	search_record_3 = models.CharField(max_length=5000,default='')
	click_record_1 = models.CharField(max_length = 5000,default='')
	bbs_friends = models.CharField(max_length=5000,default='')
	def __unicode__(self):
		return self.title
'''class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to = '/static/upload_img/', default = '/static/img/1.jpg')'''	