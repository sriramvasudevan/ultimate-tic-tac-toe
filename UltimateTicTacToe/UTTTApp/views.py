from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('index.html', locals())

def getMove(request):

    # data being received:
    # turn - 1 is X, 2 is O
    # gameOver - true/false
    # state - state of board
    # wins - who's won each large grid?
    # nextBoard - the large grid in which the move is to be played (x,y)
    # X is from L to R, Y is from top to bottom.

    # Testing GET
    coords = request.GET.getlist("nextBoard[]")
    print coords
    print request.GET.items()

    return HttpResponse("1,1,0,0")
