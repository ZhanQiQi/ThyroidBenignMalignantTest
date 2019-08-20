# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pdfmetrics.registerFont(TTFont('PingFang', 'index/static/PingFang-SC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Regular', 'index/static/font/PingFang Regular.ttf'))
pdfmetrics.registerFont(TTFont('Light', 'index/static/font/PingFang Light.ttf'))
pdfmetrics.registerFont(TTFont('Bold', 'index/static/font/PingFang Bold.ttf'))

def index(request):
    context = {}
    nodules = {}

    data = []
    data.append(nodules)

    # TODO
    # 初始化的时候，生成所有的切片（异步）,和可疑结节的信息：编号、坐标、半径，保存
    # data: nodules id and coordinates

    context['nodules'] = data
    return render(request, 'index.html', context)

def print_report(request):
    start = 0
    end = 0
    pic = ''
    ID= ''
    name = ''
    gender = ''
    age = ''
    benigin = ''
    malignant = ''
    uncertain = ''
    time = 0
    for i in range(0,len(request.path)):
        if (request.path[i] == '/') & (time == 0):
            time += 1
            begin = i
        elif (request.path[i] == '/') & (time == 1):
            time += 1
            begin = i
        elif (request.path[i] == '/') & (time == 2):
            time += 1
            pic = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 3):
            time += 1
            ID = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 4):
            time += 1
            name = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 5):
            time += 1
            gender = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 6):
            time += 1
            age = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 7):
            time += 1
            benigin = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 8):
            time += 1
            malignant = request.path[begin+1:i]
            begin = i
        elif (request.path[i] == '/') & (time == 9):
            time += 1
            uncertain = request.path[begin+1:i]
            begin = i

    print(name)
    print(age)
    print(gender)
    print(ID)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Get Data
    nodules = [{
        'pic':pic,
        'benigin':benigin,
        'malignant':malignant,
        'uncertain':uncertain,
    }]

    p = canvas.Canvas(response)
    p.setFont('Bold', 18, leading=None)
    p.drawCentredString(105 * mm, 275 * mm, "检查报告")
    p.line(20 * mm, 265 * mm, 190 * mm, 265 * mm)
    p.setFont('Regular', 10, leading=None)
    p.drawString(30 * mm, 255 * mm, "姓名：" + name)
    p.drawString(120 * mm, 255 * mm, "性别：" + gender)
    p.drawString(30 * mm, 245 * mm, "ID号：" + ID)
    p.drawString(120 * mm, 245 * mm, "年龄：" + age)
    p.line(20 * mm, 238 * mm, 190 * mm, 238 * mm)
    p.setFont('Light', 9, leading=None)
    p.drawCentredString(40 * mm, 228 * mm, "文件名")
    p.drawCentredString(90 * mm, 228 * mm, "良性")
    p.drawCentredString(120 * mm, 228 * mm, "恶性")
    p.drawCentredString(150 * mm, 228 * mm, "不确定")
    bottomY = 228
    for nodule in nodules:
        bottomY -= 10
        p.drawCentredString(40 * mm, bottomY * mm, nodule['pic'])
        p.drawCentredString(90 * mm, bottomY * mm, nodule['benigin'])
        p.drawCentredString(120 * mm, bottomY * mm, nodule['malignant'])
        p.drawCentredString(150 * mm, bottomY * mm, nodule['uncertain'])
    if bottomY > 200:
        p.line(20 * mm, 200 * mm, 190 * mm, 200 * mm)
        bottomY = 200
    else:
        p.line(20 * mm, (bottomY - 10) * mm, 190 * mm, (bottomY - 10) * mm)

    pic_fp = os.path.join(BASE_DIR, "data", nodule['pic'])
    p.drawImage(pic_fp, 80 * mm, (bottomY - 60) * mm, 50 * mm, 50 * mm)

    p.showPage()
    p.save()
    
    return response
