from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from keliu.get_data import hour

# Create your views here.

def test(request):
    x,y = hour()
    print(x,y)
    data = {
        "x": x,
        "y": y
    }
    return JsonResponse(data = data , safe=False, status=200)