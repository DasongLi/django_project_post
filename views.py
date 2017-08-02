#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os, lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from myword.form import *
from django.http import Http404, HttpResponseRedirect
# Create your views here.
from myword.models import *
from django.core.files.base import ContentFile
import SearchFiles_hupu
import SearchFiles_tianya
import cv2
import sys
import ppk,LSH,search
reload(sys)
sys.setdefaultencoding('utf-8')
'''def hex2char(hexString):
    output = hexString.decode('hex').decode('gbk').encode('utf8')
    return output'''
def search_result(request):
	global username
	if request.method == "POST":
		search_content = request.POST['Search_content']
		template = loader.get_template('search_result.html')
		length = BBS_users.objects.filter(username = username, password = password)
		if (len(length)<=0):
			user = BBS_users.objects.create(username = username, password = password)
			user.save()
		user1 = BBS_users.objects.get(username = username)
		pic = user1.photo
		'''a = [search_content]
		a = str(a)
		print(a)
		b = a[2:-1]
		print(b)
		b = b.decode('unicode-escape')
		print(b[1:-1])'''
		#a = str(unicode(search_content.decode('utf-8')).encode('gb2312'))
		#print(st1r.decode('utf-8').encode('gb2312'))
		#a = st1r.decode('utf-8').encode('gb2312')
		#a = str(a)
		#print(a)
		#print(a.decode('gb2312').encode('utf-8'))
		#print(user1.search_record_3)
		#print(user1.search_record_2.decode('gb2312').encode('utf-8'))
		#user1.search_record_3 = ""
		#user1.click_record_1 = ""
		user1.search_record_3 = user1.search_record_3 + "  " + search_content #e
		search_record_f = user1.search_record_3.split("  ")
		for i in search_record_f:
			print(i)
		click_record_f = user1.click_record_1.split("*****")
		print(click_record_f)
		print(search_record_f)
		for j in click_record_f:
			print(j)
		user1.save()
		print(pic)
		if pic !="/static/img/1.jpg":
			img = "/media/" + str(pic)
		else:
			img = "/static/img/1.jpg"
		BBS1 = BBS_users.objects.all()
		P = dict()
		for item in BBS1:
			if item.username != '':
				#user_s = BBS_users.objects.get(username = username)
				search_record_f = item.search_record_3.split("  ")
				click_record_f = item.click_record_1.split("*****")
				search_record_f_f = []
				click_record_f_f = []
				for item1 in search_record_f: 
					if item1 != '':
						search_record_f_f.append(item1+"***")
				for item2 in click_record_f:
					if item2 != '':
						click_record_f_f.append(item2+"^&^")
				P[item.username] = search_record_f_f + click_record_f_f
		#print(P)
		'''for i,j in P.items():
			print(i)
			for item in j:
				print(item)'''
		p_dict = ppk.sort(ppk.personal_pk(P,username,0.85,50))
		user_recommend_list = []
		search_recommend_list = []
		click_recommend_list = []
		a = 0
		b = 0
		c = 0
		for i in p_dict:
			if i[0][-3:] != '***' and i[0][-3:] != '^&^':
				if i[0]!= username :
					user_recommend_list.append(i[0])
					a = a + 1
			elif i[0][-3:] =='***':
				search_record_fs = user1.search_record_3.split("  ")
				if i[0][:-3] not in search_record_fs and b<4:
					search_recommend_list.append(i[0][:-3])
					b = b + 1
			elif i[0][-3:] == '^&^' and c<8:
				click_record_fs = user1.click_record_1.split("*****")
				if i[0][:-3] not in click_record_fs:
					click_recommend_list.append(i[0][:-3])
					c = c + 1
		bbs_user_all = []
		bbs_user_s_s = []
		dsd = 0
		for item in user_recommend_list:
			if dsd<8:
				user_i = BBS_users.objects.get(username = item)
				bbs_user_s_s.append(item)
				bbs_user_s_s.append(user_i.signature)
				pic_i = user_i.photo
				if pic_i !="/static/img/1.jpg":
					img_i = "/media/" + str(pic_i)
				else:
					img_i = "/static/img/1.jpg"
				bbs_user_s_s.append(img_i)
				bbs_user_all.append(bbs_user_s_s)
				bbs_user_s_s = []
				dsd = dsd + 1
		result_s_s_s = search.init_search(search_content,vm_env)
		result_s = SearchFiles_hupu.init_search(search_content,vm_env)
		result_s_s = SearchFiles_tianya.init_search(search_content,vm_env)
		context = {
			#'a':[1,2,3],'b':[4,5,6],'c':[7,8,9],
			's':search_content,
			'login_out':'login out',
			'edit_you':'edit you',
			'username':user1.username,
			'img':img,'register':'change user',
			'signature':user1.signature,
			'logout_href':'/login/',
			'change_user_href':'/login/',
			'result_s':result_s,
			'result_s_s':result_s_s,
			'bbs_user_all':bbs_user_all,
			'click_recommend':click_recommend_list,
			'search_recommend':search_recommend_list,
			'result_s_s_s':result_s_s_s,
		}
		return HttpResponse(template.render(context,request))
def picture_search(request):
	global username
	if request.method == "POST":
		#photo=request.FILES['photo']
		#print(photo)
		#cv2.imwrite("/static/upload_img/target.jpg",photo)
		#signature = request.POST['signature']
		file_content = ContentFile(request.FILES['img'].read())
		photo = request.FILES['img']
		print(photo)
		user = Picture_search.objects.create(photo = photo)
		user.save()
		'''user2 = BBS_users.objects.get(username = username)
		user2.signature = signature
		user2.photo =request.FILES['img']
        #img = ImageStore(name = request.FILES['img'].name, img =request.FILES['img'])  
    	#img.save()
    	user2.save()'''
    	pic_list = LSH.LSH("/home/lds/Documents/django_project/Helloworld/media/search_file/"+str(photo))
    	for i in range(len(pic_list)):
  			pic_list[i] = pic_list[i][:-4]
    	user1 = BBS_users.objects.get(username = username)
    	template = loader.get_template('picture_result.html')
    	context = {
    		'login_out':'login out',
			'edit_you':'edit you',
			'username':user1.username,
			'img':img,'register':'change user',
			'signature':user1.signature,
			'logout_href':'/login/',
			'change_user_href':'/login/',
			'pic_list':pic_list,
    	}
    	return HttpResponse(template.render(context,request))
def record_bbs(request,title):
	global username
	user1 = BBS_users.objects.get(username = username)
	#user1.click_record_1 = ''
	user1.click_record_1 = user1.click_record_1 + "*****" +str(title)
	user1.save()
	bbs = BBS_hupu_tianya.objects.get(title = title)
	print(bbs.url)
	return HttpResponseRedirect(bbs.url)
def post_comment(request,rank_id1):
	global username
	bbs_page = BBS.objects.get(rank_id = rank_id1)
	comment = request.POST['comment_form']
	author_add_comment = comment + "AAA" + username + "***"
	bbs_page.comment_others = bbs_page.comment_others + author_add_comment
	bbs_page.save()
	return HttpResponseRedirect('/details/' + str(rank_id1))
def add_friends(request,friend_name):
	global username
	user1 = BBS_users.objects.get(username = username)
	user1.bbs_friends = user1.bbs_friends + " " + friend_name 
	print(user1.bbs_friends)
	user1.save()
	return HttpResponseRedirect('/main/')
def details(request,rank_id1):
	#text = "Displaying article Number : %s" %rank_id1
	#return HttpResponse(text)
	global username
	bbs_page = BBS.objects.get(rank_id = rank_id1)
	bbs_page_id = []
	bbs_page_id.append(bbs_page.title)
	bbs_page_id.append(bbs_page.summary)
	bbs_page_id.append(bbs_page.content)
	bbs_page_id.append(bbs_page.author)
	#print(bbs_page_id)
	user1 = BBS_users.objects.get(username = username)
	#user1.click_record_1 = ''
	user1.click_record_1 = user1.click_record_1 + "*****" + str(bbs_page.title)
	print(user1.click_record_1)
	user1.save()
	pic = user1.photo
	print(pic)
	bbs_comment = bbs_page.comment_others
	bbs_comment_each = []
	bbs_comment_all = []
	bbs_comment_1 = bbs_comment.split('***')
	print(bbs_comment_1)
	print(bbs_comment)
	for ele in bbs_comment_1:
		if len(ele) >= 1:
			a = ele.split('AAA')
			#print(a)
			bbs_comment_each.append(a[0])
			user2 = BBS_users.objects.get(username = a[1])
			pic = user2.photo
			if pic !="/static/img/1.jpg":
				img = "/media/" + str(pic)
			else:
				img = "/static/img/1.jpg"
			bbs_comment_each.append(img)
			bbs_comment_each.append(a[1])
			bbs_comment_all.append(bbs_comment_each)
			bbs_comment_each = []
	if pic !="/static/img/1.jpg":
		img = "/media/" + str(pic)
	else:
		img = "/static/img/1.jpg"
	template = loader.get_template('details.html')
	context = {
		'bbs_comment':bbs_comment_all,
		'bbs_content':bbs_page_id,
		'login_out':'login out',
		'edit_you':'edit you',
		'username':user1.username,
		'img':img,'register':'change user',
		'signature':user1.signature,
		'logout_href':'/login/',
		'change_user_href':'/login/',
		'bbs_id':rank_id1,
	}
	return HttpResponse(template.render(context,request))	
def post(request):
	global username
	if request.method == "POST":
		title = request.POST['title']
		summary = request.POST['summary']
		comment = request.POST['comment']
		author = username
		'''a = [search_content]
		a = str(a)
		print(a)
		b = a[2:-1]
		print(b)
		b = b.decode('unicode-escape')
		print(b[1:-1])'''
		'''title_1 = [title]
		summary_1 = [summary]
		comment_1 = [comment]
		title_1 = str(title_1)
		summary_1 = str(summary_1)
		comment_1 = str(comment_1)
		print(summary_1)
		print(comment_1)
		print(title_1)
		title_3 = "a "+title_1
		comment_3 = "b "+comment_1
		summary_3 = "c "+ summary_1'''
		'''title_2 = title_1[2:-1]
		summary_2 = summary_1[2:-1]
		comment_2 = comment_1[2:-1]
		print(title_2)'''
		'''title_2 = title_2.decode('unicode-escape')
		summary_2 = summary_2.decode('unicode-escape')
		comment_2 = comment_2.decode('unicode-escape')
		title_2 = title_2[1:-1]
		summary_2 = summary_2[1:-1]
		comment_2 = comment_2[1:-1]'''
		filterResult = BBS.objects.filter(title = title)
		if len(filterResult)<=0:
			rank_id1 = 1
			bbs = BBS.objects.all()
			for bbs_s in bbs:
				rank_id1 = rank_id1 + 1
			user = BBS.objects.create(author=username,rank_id = rank_id1,title =title,summary = summary,content = comment)
			user.save()
			return HttpResponseRedirect('/main/')
		else:
			template = loader.get_template('post.html')
			context = {'post':""}
			return HttpResponse(template.render(context,request))
	else:
		user1 = BBS_users.objects.get(username = username)
		pic = user1.photo
		print(pic)
		if pic !="/static/img/1.jpg":
			img = "/media/" + str(pic)
		else:
			img = "/static/img/1.jpg"
		template = loader.get_template('post.html')
		context = {
			'login_out':'login out',
			'edit_you':'edit you',
			'username':user1.username,
			'img':img,'register':'change user',
			'signature':user1.signature,
			'logout_href':'/login/',
			'change_user_href':'/login/',
		}
		return HttpResponse(template.render(context,request))
def change_info(request):
	global username
	user1 = BBS_users.objects.get(username = username)
	pic = user1.photo
	friend = user1.bbs_friends
	friends = friend.split(' ')
	print(friend)
	print(friends)
	friends_s = []
	friend_detail = []
	for item in friends:
		if len(item)>0:
			friend_detail = []
			user2 =  BBS_users.objects.get(username = item)
			pic = user2.photo
			if pic !="/static/img/1.jpg":
				img = "/media/" + str(pic)
			else:
				img = "/static/img/1.jpg"
			friend_detail.append(item)
			friend_detail.append(img)
			friends_s.append(friend_detail)
	#print(friends_s)
	#print(pic)
	if pic !="/static/img/1.jpg":
		img = "/media/" + str(pic)
	else:
		img = "/static/img/1.jpg"
	template = loader.get_template('post.html')
	context = {
		'login_out':'login out',
		'edit_you':'edit you',
		'username':user1.username,
		'img':img,'register':'change user',
		'signature':user1.signature,
		'logout_href':'/login/',
		'change_user_href':'/login/',
		'friends':friends_s,
	}
	template = loader.get_template('change_info.html')
	return HttpResponse(template.render(context,request))
def homepage_other(request,name):
	global username
	user1 = BBS_users.objects.get(username = username)
	pic = user1.photo
	'''friend = user1.bbs_friends
	friends = friend.split(' ')
	print(friend)
	print(friends)
	friends_s = []
	friend_detail = []
	for item in friends:
		if len(item)>0:
			friend_detail = []
			user2 =  BBS_users.objects.get(username = item)
			pic = user2.photo
			if pic !="/static/img/1.jpg":
				img = "/media/" + str(pic)
			else:
				img = "/static/img/1.jpg"
			friend_detail.append(item)
			friend_detail.append(img)
			friends_s.append(friend_detail)'''
	#print(friends_s)
	#print(pic)
	user2 = BBS_users.objects.get(username = name)
	pic2 = user2.photo
	if pic2 !="/static/img/1.jpg":
		img2 = "/media/" + str(pic2)
	else:
		img2 = "/static/img/1.jpg"
	if pic !="/static/img/1.jpg":
		img = "/media/" + str(pic)
	else:
		img = "/static/img/1.jpg"
	bbs = BBS.objects.all()
	user_bbs_1 = []
	user_bbs_s = []
	for ele in bbs:
		if ele.author == user2.username:
			#print(ele.author)
			user_bbs_s.append(ele.content)
			user_bbs_s.append(ele.title)
			user_bbs_s.append(ele.summary)
			user_bbs_s.append(ele.rank_id)
			user_bbs_1.append(user_bbs_s)
			user_bbs_s = []
	context = {
		'login_out':'login out',
		'edit_you':'edit you',
		'username':user1.username,
		'img':img,'register':'change user',
		'signature':user1.signature,
		'logout_href':'/login/',
		'change_user_href':'/login/',
		'user2_name':user2.username,
		'user2_signature':user2.signature,
		'user2_pic':img2,
		'user_bbs_s':user_bbs_1,
	}
	template = loader.get_template('homepage_others.html')
	return HttpResponse(template.render(context,request))
def update(request):
	global username
	if request.method == "POST":
		#photo=request.FILES['photo']
		#print(photo)
		#cv2.imwrite("/static/upload_img/target.jpg",photo)
		signature = request.POST['signature']
		file_content = ContentFile(request.FILES['img'].read())
		user2 = BBS_users.objects.get(username = username)
		user2.signature = signature
		user2.photo =request.FILES['img']
        #img = ImageStore(name = request.FILES['img'].name, img =request.FILES['img'])  
    	#img.save()
    	user2.save()
    	'''template = loader.get_template('success.html')
    	context = {'img':user2.photo, 'signature':user2.signature}
    	return HttpResponse(template.render(context,request))'''
    	return HttpResponseRedirect('/main/')
    	#return HttpResponse('上传成功')
	'''else:
		print("23")
		return HttpResponse('上传失败')'''
def success(request):
	global password
	global username
	global img
	global user_type
	#print(password)
	'''BBS_user = BBS_users()
	BBS_user.password = password
	BBS_user.username = username'''
	#all_entries = BBS.objects.all()
	#print(all_entries)
	a = []
	b = []
	c = []
	s = []
	s_s = []
	#BBS.objects.filter(author = 'chenghongjie').delete()
	#BBS.objects.all().delete()
	bbs = BBS.objects.all()
	bbs_user_all = []
	bbs_user_s_s = []
	BBS1 = BBS_users.objects.all()
	ab = 0
	for bbs_user_s in BBS1:
		if bbs_user_s.username != '' and ab<6:
			bbs_user_s_s.append(bbs_user_s.username)
			bbs_user_s_s.append(bbs_user_s.signature)
			pic = bbs_user_s.photo
			if pic !="/static/img/1.jpg":
				img = "/media/" + str(pic)
			else:
				img = "/static/img/1.jpg"
			bbs_user_s_s.append(img)
			bbs_user_all.append(bbs_user_s_s)
			'''print(bbs_user_s.username)
			print(bbs_user_s.signature)
			print(bbs_user_s.photo)'''
			ab = ab + 1
			bbs_user_s_s = []
	for bbs_s in bbs:
		s.append(bbs_s.title)
		s.append(bbs_s.summary)
		s.append(bbs_s.content)
		s.append(bbs_s.rank_id)
		#print(bbs_s.rank_id)
		'''print(bbs_s.title)
		print(bbs_s.summary)
		print(bbs_s.content)'''
		s_s.append(s)
		s = []
	'''for i in range(1):
		#ab = BBs()
		bbs = BBS.objects.get(rank_id = i+1)
		a.append(bbs.title)
		b.append(bbs.summary)
		c.append(bbs.content)
		s.append(bbs.title)
		s.append(bbs.summary)
		s.append(bbs.content)
		s_s.append(s)
		ab.title = bbs.title
		ab.summary = bbs.summary
		ab.content = bbs.content
		s.append(ab)
	print(s)'''

	if (len(username)>0 or user_type!=0):
		user_type = 1
		length = BBS_users.objects.filter(username = username, password = password)
		if (len(length)<=0):
			user = BBS_users.objects.create(username = username, password = password)
			user.save()
		user1 = BBS_users.objects.get(username = username)
		pic = user1.photo
		print(pic)
		if pic !="/static/img/1.jpg":
			img = "/media/" + str(pic)
		else:
			img = "/static/img/1.jpg"
		user1.save()
		#print(a[0])
		#print(b[0])
		#print(c[0])

		template = loader.get_template('success.html')
		context = {
			#'a':[1,2,3],'b':[4,5,6],'c':[7,8,9],
			's1':bbs_user_all,
			's':s_s,
			'login_out':'login out',
			'edit_you':'edit you',
			'username':user1.username,
			'img':img,'register':'change user',
			'signature':user1.signature,
			'logout_href':'/login/',
			'change_user_href':'/login/',
		}
		return HttpResponse(template.render(context,request))
	else:
		img = "/static/img/IEEE.jpeg"
		template = loader.get_template('success.html')
		context = {
			's':s_s,
			'login_out':'register',
			'edit_you':'edit you','username':'',
			'img':img,'register':'login' ,
			'signature':'',
			'logout_href':'/register/',
			'change_user_href':'/login/',
		}
		return HttpResponse(template.render(context,request))
def h1(request):
	if request.method == 'POST':
		form = Mybook(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			title = data['title']
		return HttpResponse(title)
	form = Mybook()
	template = loader.get_template('form.html')
	context = {'form':form,}
	return HttpResponse(template.render(context,request))
def vie(request):
	template = loader.get_template('1.html')
	context = {'ab':"fdfsdfsd",}
	return HttpResponse(template.render(context,request))
	#return render_to_response('1.html',{"name":"hello23"})
def index(request):
	return HttpResponse("Hello world")
def index1(request,num):
	try:
		num = int(num)
		return HttpResponse("hello"+str(num))
	except ValueError:
		raise Http404()
def login(request):
	global username
	global password
	if request.method == "POST":
		#uf = UserFormLogin(request.POST)
		#if uf.is_valid():
   		#获取表单信息
   		if 'username' in request.POST:
   			username = request.POST['username']
   			password = request.POST['password1']   
   			userResult = Users.objects.filter(username=username,password=password)
	   		#pdb.set_trace()
	   		if (len(userResult)>0):
				return HttpResponseRedirect('/main/')
	   		else:
	   			return HttpResponse("该用户不存在 or wrong password")
 	else:
  		uf = UserFormLogin()
	template = loader.get_template('UserFormLogin.html')
	context = {'uf':"uf",}
	return HttpResponse(template.render(context,request))
def register(request):
	if request.method == "POST":
		#uf = UserForm(request.POST)
		'''if uf.is_valid():
			username = uf.cleaned_data['username']'''
		if 'username' in request.POST:
			username = request.POST['username']
			filterResult = Users.objects.filter(username = username)
			if len(filterResult)>0:
				return HttpResponse("errors")
			else:
				password1 = request.POST['password1']
				password2 = request.POST['password2']
				errors = []
				if (password2 != password1):
					errors.append("noe")
					return HttpResponse("nie")
				password = password1
				email = request.POST['email']
				user = Users.objects.create(username=username,password=password1)
				user.save()
				return HttpResponseRedirect('/login/')
				'''template = loader.get_template('UserFormLogin.html')
				context = {'username':username,}
				return HttpResponse(template.render(context,request))'''
	'''else:
		uf = UserForm()'''
	template = loader.get_template('register.html')
	context = {'uf':"uf",}
	return HttpResponse(template.render(context,request))
class UserForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=100)
	password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
	password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
	email = forms.EmailField(label='电子邮件')
class UserFormLogin(forms.Form):
	username = forms.CharField(label='用户名',max_length=100)
	password = forms.CharField(label='密码',widget=forms.PasswordInput())
class BBs():
	title = ''
	summary = ''
	content = ''
password = ""
email = ""
username = ""
img = ""
user_type = 0
vm_env = lucene.initVM()
'''user23 = Users.objects.create(username="lds",password="123456")
user23.save()'''