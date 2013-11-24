from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('index.html', locals())

def getMove(request):
    return HttpResponse("1,1,0,0")
