from django.http import HttpResponse
from django.shortcuts import render_to_response
import random

#Defining global variables.
turn = 0
state = []
wins = []
nextboard = []
playanywhere = False

#Get a list of all the empty squares in the sub- grid
def GetEmptySquares(x,y):

    toReturn = []
    for i in range(3):
        for j in range(3):
            if state[x][y][i][j] == 0:
                toReturn.append([i,j])
    return toReturn

def GetValidMoves():
    return GetEmptySquares(nextboard[0],nextboard[1])

def Amateur():
    """The amateur difficulty. Random bot."""
    ValidMoves = GetValidMoves()
    r = random.randint(0,len(ValidMoves)-1)
    toReturn = str(nextboard[0]) + ',' + str(nextboard[1]) + ',' + str(ValidMoves[r][0]) + ',' + str(ValidMoves[r][1])
    return HttpResponse(toReturn)
    

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
    global turn
    global state
    global wins
    global nextboard
    turn = request.GET["turn"]
    nextboard = ([int(a) for a in request.GET.getlist("nextBoard[]")])
    state = []
    for i in range(3):
        state.append([])
        for j in range(3):
            state[i].append([])
            for k in range(3):
                argstring = "state["+str(i)+"]["+str(j)+"]["+str(k)+"][]"
                state[i][j].append([int(a) for a in request.GET.getlist(argstring)])
                for element in state[i][j][k]:
                    element = int(element)

    for i in range(3):
        wins.append([])
        argstring = "wins[" + str(i) + "][]"
        wins[i].append([int(a) for a in request.GET.getlist(argstring)])
    diff = int(request.GET["difficulty"])
    if diff == 0:
        return Amateur()
    if diff == 1:
        return Professional()
    else:
        return Legendary()
