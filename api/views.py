from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from keliu.get_data import hour, newest_record

# Create your views here.

def get_hour_num(request):
    mydate = request.GET['date']
    if len(mydate) == 0:
        mydate = newest_record()
        x, y = hour(mydate)
    else:
        mydate = request.GET['date'].replace('-', '/')
        x, y = hour(mydate)

    #列表元素求和，算出总人数
    sum = 0
    for index in range(0,len(y)):
        sum = sum + y[index]

    data = {
        "x": x,
        "y": y,
        "d": mydate,
        "s": sum
    }
    return JsonResponse(data = data , safe=False, status=200)