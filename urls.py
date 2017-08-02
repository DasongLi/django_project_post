"""Helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views import *
from myword import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
	url(r'^hello/',views.index),
	url(r'^hello/(\d+)/',views.index1),
	url(r'^tem/',views.vie),
    url(r'^admin/', admin.site.urls),
    url(r'^mybook/',views.h1),
    url(r'^register/',views.register),
    url(r'^login/',views.login),
    url(r'^main/',views.success),
    url(r'^change_info/',views.change_info),
    url(r'^update/',views.update),
    url(r'^post/',views.post),
    url(r'^search_result/',views.search_result),
    url(r'^details/(\d+)',views.details),
    url(r'^add_friend/(.+)',views.add_friends),
    url(r'^post_comment/(\d+)',views.post_comment),
    url(r'^homepage/(.+)',views.homepage_other),
    url(r'^record_bbs/(.+)',views.record_bbs),
    url(r'^picture_search/',views.picture_search),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)