# -*- coding: utf-8 -*-

from django.http import JsonResponse
import load
from ..settings import BASE_DIR
import os


def load_img(request):
    print(request)
    res = {}
    file_name = request.POST.get('src')
    mhd_file = os.path.join(BASE_DIR, "data/" + str(file_name))
    if os.path.isfile(mhd_file):
        save_path = os.path.join(BASE_DIR, "index/static/image")
        cnt = load.load_img(mhd_file, save_path)
        res['max_cnt'] = cnt
        print(request.POST.get('src'))

    return JsonResponse(res)


def load_nodules(request):
    file_name = request.GET['src']
    mhd_file = os.path.join(BASE_DIR, "data/" + str(file_name))
    res = {}
    if file_name == "1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860.mhd":
        res = {'nodules': [
            {'x': 44, 'y': 211, 'z': 77},
            {'x': 405, 'y': 154, 'z': 117},
        ]}
    else:
        if file_name == "1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405.mhd":
            res = {'nodules': [
                {'x': 220, 'y': 292, 'z': 251},
                {'x': 379, 'y': 250, 'z': 230},
                {'x': 376, 'y': 335, 'z': 141},
            ]}
    return JsonResponse(res)
