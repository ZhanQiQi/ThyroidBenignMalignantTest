"""iLabNodules URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.conf.urls import url
from . import views
from data_proc import ajax_test
from data_proc import upload
from data_proc import img_proc

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ajax_list/$', ajax_test.ajax_list, name='ajax_list'),
    url(r'^ajax_dict/$', ajax_test.ajax_dict, name='ajax_dict'),
    url(r'^load_img/$', img_proc.load_img, name='load_img'),
    url(r'^load_nodules/$', img_proc.load_nodules, name='load_nodules'),
    url(r'^upload/$', upload.upload, name='upload'),
    url(r'^ai_treat/$', upload.ai_treat, name='ai_treat'),  
    url(r'^load/$', upload.load, name='load'),  
    url(r'^print_report/[\s\S]*/$', views.print_report, name='print_report')
]
