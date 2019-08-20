# -*- coding: utf-8 -*-
from django.http import HttpResponse,JsonResponse
import os
from ..settings import BASE_DIR
import SimpleITK
import scipy.misc as misc
import os
from thyroid_detection import primary_detect


def upload(request):
    print("parsing.")
    if not request.method == "POST":
        print("please use POST method!")
        return HttpResponse("please use POST method!")
    else:
        my_file = request.FILES.get("upload", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not my_file:
            print("No files for upload!")
            return HttpResponse("No files for upload!")
        else:
            # 打开特定的文件进行二进制的写操作
            destination = open(os.path.join(BASE_DIR, "data/" + str(my_file.name)), 'wb+')
            # 分块写入文件
            for chunk in my_file.chunks():
                destination.write(chunk)
            destination.close()
            print("upload suc! the file name is " + str(my_file.name))
            return HttpResponse(str(my_file.name))

def load(request):
    pic = request.GET['pic']
    pic_fp = os.path.join(BASE_DIR, "data", pic)
    if not os.path.exists(pic_fp):
        return JsonResponse(dict(status='error', msg='{} not exist'.format(pic)))
    pic_file = open(pic_fp, 'r').read()
    print(pic_file)
    return HttpResponse(pic_file)


def my_super_ai_function(pic_fp):
    res = ['No', 'No', 'No']
    res[primary_detect(pic_fp)[0]] = 'Yes'
    return res


def ai_treat(request):
    pic = request.GET['pic']
    pic_fp = os.path.join(BASE_DIR, "data", pic)
    if not os.path.exists(pic_fp):
        return JsonResponse(dict(status='error', msg='{} not exist'.format(pic)))
    # do something here
    res = my_super_ai_function(pic_fp=pic_fp)
    return JsonResponse(dict(status='success', data=res))




