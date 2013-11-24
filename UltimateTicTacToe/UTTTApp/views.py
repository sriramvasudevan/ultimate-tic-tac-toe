from django.http import HttpResponse
from django.shortcuts import render_to_response
import random
import copy

#Defining global variables.
turn = 0
state = []
wins = []
#Must never access nextboard if playanywhere is True.
nextboard = []
playanywhere = False

LARGE = 1000

#Helper functions
def WhoseSubBoard(board,x,y):

    #If it's won already in wins, no point in us re-examining it.
    if wins[x][y] != 0:
        return wins[x][y]

    sb = board[x][y]
    #Checking for X
    #Vertical.
    if sb[0][0] == 1 and sb[1][0] == 1 and sb[2][0] == 1:
        return 1
    if sb[0][1] == 1 and sb[1][1] == 1 and sb[2][1] == 1:
        return 1
    if sb[0][2] == 1 and sb[1][2] == 1 and sb[2][2] == 1:
        return 1
    #Horizontal
    if sb[0][0] == 1 and sb[0][1] == 1 and sb[0][2] == 1:
        return 1
    if sb[1][0] == 1 and sb[1][1] == 1 and sb[1][2] == 1:
        return 1
    if sb[2][0] == 1 and sb[2][1] == 1 and sb[2][2] == 1:
        return 1
    #Diagonal
    if sb[0][0] == 1 and sb[1][1] == 1 and sb[2][2] == 1:
        return 1
    if sb[0][2] == 1 and sb[1][1] == 1 and sb[2][0] == 1:
        return 1
    #Checking for 0
    #Vertical.
    if sb[0][0] == 2 and sb[1][0] == 2 and sb[2][0] == 2:
        return 1
    if sb[0][1] == 2 and sb[1][1] == 2 and sb[2][1] == 2:
        return 2
    if sb[0][2] == 2 and sb[1][2] == 2 and sb[2][2] == 2:
        return 2
    #Horizontal
    if sb[0][0] == 2 and sb[0][1] == 2 and sb[0][2] == 2:
        return 2
    if sb[1][0] == 2 and sb[1][1] == 2 and sb[1][2] == 2:
        return 2
    if sb[2][0] == 2 and sb[2][1] == 2 and sb[2][2] == 2:
        return 2
    #Diagonal
    if sb[0][0] == 2 and sb[1][1] == 2 and sb[2][2] == 2:
        return 2
    if sb[0][2] == 2 and sb[1][1] == 2 and sb[2][0] == 2:
        return 2

    return 0

def other(t):
    """Similar to Slinky's other(turn) function"""
    if t == 1:
        return 2
    return 1
    
#Subevaluation functions. Board is a 4-D array.

#Bonus for winning subboards.
def WonSubBoards(board):
    
    #The weight for this.
    WONSB_BONUS = 10
    toReturn = 0
    for i in range(3):
        for j in range(3):
            temp = WhoseSubBoard(board,i,j)
            if temp == turn:
                toReturn += WONSB_BONUS
            elif temp == other(turn):
                toReturn -= WONSB_BONUS
    return toReturn

#Evaluation function.
def Evaluate(board):
    
    toReturn = 0
    toReturn += WonSubBoards(board)

    return toReturn


#Get a list of all the empty squares in the sub- grid
def GetEmptySquares(x,y):

    toReturn = []
    for i in range(3):
        for j in range(3):
            if state[x][y][i][j] == 0:
                toReturn.append([x,y,i,j])
    return toReturn

def GetValidMoves():
    if playanywhere:
        toReturn = []
        for i in range(3):
            for j in range(3):
                toReturn.extend(GetEmptySquares(i,j))
        return toReturn
    else:
        return GetEmptySquares(nextboard[0],nextboard[1])

def Amateur():
    """The amateur difficulty. Random bot."""
    ValidMoves = GetValidMoves()
    r = random.randint(0,len(ValidMoves)-1)
    toReturn = str(ValidMoves[r][0]) + ',' + str(ValidMoves[r][1]) + ',' + str(ValidMoves[r][2]) + ',' + str(ValidMoves[r][3])
    return HttpResponse(toReturn)

def Professional():
    """The professional difficulty. Just evaluates, no lookahead."""
    ValidMoves = GetValidMoves()
    highest = -LARGE
    bestmove = None
    for move in ValidMoves:
        newboard = copy.deepcopy(state) 
        newboard[move[0]][move[1]][move[2]][move[3]] = turn
        value = Evaluate(newboard)
        if value > highest:
            highest = value
            bestmove = move
        del newboard
    toReturn = str(bestmove[0]) + ',' + str(bestmove[1]) + ',' + str(bestmove[2]) + ',' + str(bestmove[3])
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
    if request.GET["nextBoard[]"] == 'null':
        playanywhere = True
    else:
        nextboard = ([int(a) for a in request.GET.getlist("nextBoard[]")])
        playanywhere = False
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
    wins = []
    for i in range(3):
        argstring = "wins[" + str(i) + "][]"
        wins.append([int(a) for a in request.GET.getlist(argstring)])
    diff = int(request.GET["difficulty"])
    if diff == 0:
        return Amateur()
    if diff == 1:
        return Professional()
    else:
        return Legendary()
