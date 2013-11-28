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


def TwoOfThree(tl, which):
    """Returns true if 2 of the three elements in threelist are which, and the third is 0."""
    return tl.count(which) == 2 and tl.count(0) == 1

    
def AlmostWonCount(board,x,y):    
    """If 2 out of 3 in any row, column or diagonal are ours, and the third is blank, add. Do the same
        for the opponent. Return (number of ours - number of theirs) found.
    """

    toReturn = 0
    sb = board[x][y]
    #Define threelists and keep sending.
    #Verticals
    tl = [sb[0][0],sb[1][0],sb[2][0]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    tl = [sb[0][1],sb[1][1],sb[2][1]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    tl = [sb[0][2],sb[1][2],sb[2][2]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1

    #Horizontals.
    tl = [sb[0][0],sb[0][1],sb[0][2]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    tl = [sb[1][0],sb[1][1],sb[1][2]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    tl = [sb[2][0],sb[2][1],sb[2][2]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    #Diagonals.
    tl = [sb[0][0],sb[1][1],sb[2][2]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1
    tl = [sb[0][2],sb[1][1],sb[2][0]]
    if TwoOfThree(tl,turn):
        toReturn += 1
    if TwoOfThree(tl,other(turn)):
        toReturn -= 1

    # print toReturn
    return toReturn 

    
#Subevaluation functions. Board is a 4-D array.

#Bonus for winning subboards.
#Returns the boards that haven't been won for the use of the remaining sub-eval functions.
def WonSubBoards(board):
    
    #The weight for this.
    WONSB_BONUS = 20
    toReturn = 0
    notwonlist = []
    for i in range(3):
        for j in range(3):
            temp = WhoseSubBoard(board,i,j)
            if temp == turn:
                toReturn += WONSB_BONUS
            elif temp == other(turn):
                toReturn -= WONSB_BONUS
            else:
                notwonlist.append([i,j])

    return (toReturn,notwonlist)


#Are all 3 elements in threelist = 3?
def ThreeEqual(threelist,which):
    assert len(threelist) == 3
    return threelist.count(which)==3


#Is the game over?
def IsGameOver(board):

    wonlist = []
    for i in range(3):
        wonlist.append([])
        for j in range(3):
            wonlist[i].append(WhoseSubBoard(board,i,j))
    tl = [wonlist[0][0],wonlist[1][0],wonlist[2][0]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))
    tl = [wonlist[0][1],wonlist[1][1],wonlist[2][1]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))
    tl = [wonlist[0][2],wonlist[1][2],wonlist[2][2]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))

    #Horizontals.
    tl = [wonlist[0][0],wonlist[0][1],wonlist[0][2]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))
    tl = [wonlist[1][0],wonlist[1][1],wonlist[1][2]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))
    tl = [wonlist[2][0],wonlist[2][1],wonlist[2][2]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))

    #Diagonals.
    tl = [wonlist[0][0],wonlist[1][1],wonlist[2][2]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))
    tl = [wonlist[0][2],wonlist[1][1],wonlist[2][0]]
    if ThreeEqual(tl,turn):
        return (True,turn)
    if ThreeEqual(tl,other(turn)):
        return (True,other(turn))

    return (False,0)


def AlmostWonSubBoards(board,notwonlist):

    #The weight for this.
    ALMOSTWONSB_BONUS = 3
    toReturn = 0
    for sb in notwonlist:
        toReturn += ALMOSTWONSB_BONUS*AlmostWonCount(board,sb[0],sb[1])
    return toReturn


#Evaluation function.
def Evaluate(board):
    
    toReturn = 0
    (wsb,notwonlist) = WonSubBoards(board)
    toReturn += wsb
    toReturn += AlmostWonSubBoards(board,notwonlist)
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
    '''Gets a list of valid moves, given the current state and turn'''

    global playanywhere
    if playanywhere:
        toReturn = []
        for i in range(3):
            for j in range(3):
                toReturn.extend(GetEmptySquares(i,j))
        return toReturn
    else:
        return GetEmptySquares(nextboard[0],nextboard[1])


def GetEmptySquares_AB(board,x,y):

    toReturn = []
    for i in range(3):
        for j in range(3):
            if board[x][y][i][j] == 0:
                toReturn.append([x,y,i,j])
    return toReturn


#Defining a separate GetValidMoves() for AB, because it's faster.
#Add the play_anywhere and shit here.
def GetValidMoves_AB(board,next_board):
    
    next_board_valid = GetEmptySquares_AB(board,next_board[0], next_board[1])
    if len(next_board_valid) == 0 or WhoseSubBoard(board,next_board[0],nextboard[1]) != 0:
        toReturn = []
        for i in range(3):
            for j in range(3):
                toReturn.extend(GetEmptySquares_AB(board,i,j))
        return toReturn
    else:
        return next_board_valid


# The alpha-beta algorithm
def AlphaBeta(board, depth, alpha, beta, ourturn, nboard):

    (gameover,winner) = IsGameOver(board)
    if gameover:
        if winner == turn:
            return LARGE
        else:
            return -LARGE
    if depth == 0:
        return Evaluate(board)

    if ourturn:
        moves = GetValidMoves_AB(board,nboard)
        for move in moves:
            newboard = copy.deepcopy(board)
            newboard[move[0]][move[1]][move[2]][move[3]] = turn
            value = AlphaBeta(newboard,depth-1,alpha,beta,False,[move[2],move[3]])
            if value > alpha:
                alpha = value

            if beta <= alpha:
                return beta
        return alpha
    else:
        moves = GetValidMoves_AB(board,nboard)
        for move in moves:
            newboard = copy.deepcopy(board)
            newboard[move[0]][move[1]][move[2]][move[3]] = other(turn)

            value = AlphaBeta(newboard,depth-1,alpha,beta,True,[move[2],move[3]])
            if value < beta:
                beta = value
            if beta <= alpha:
                return alpha
        return beta


def Amateur():
    """The amateur difficulty. Random bot."""
    ValidMoves = GetValidMoves()
    r = random.randint(0,len(ValidMoves)-1)

    # Preparing the move to return - [X,Y,x,y] where the first two are coords of the subboard within the board
    # and the next two are the coords of the tic tac toe square to be played, within the (X,Y) subboard.
    toReturn = str(ValidMoves[r][0]) + ',' + str(ValidMoves[r][1]) + ',' + str(ValidMoves[r][2]) + ',' + str(ValidMoves[r][3])
    return HttpResponse(toReturn)


def Professional():
    """The professional difficulty. Just evaluates, no lookahead."""
    ValidMoves = GetValidMoves()
    highest = -LARGE
    bestmove = None

    # Iterate over all valid moves, evaluate each one of them
    for move in ValidMoves:
        newboard = copy.deepcopy(state) 
        newboard[move[0]][move[1]][move[2]][move[3]] = turn
        value = Evaluate(newboard)
        if value > highest:
            highest = value
            bestmove = move
        del newboard

    # Preparing the move to return - [X,Y,x,y] where the first two are coords of the subboard within the board
    # and the next two are the coords of the tic tac toe square to be played, within the (X,Y) subboard.
    toReturn = str(bestmove[0]) + ',' + str(bestmove[1]) + ',' + str(bestmove[2]) + ',' + str(bestmove[3])
    return HttpResponse(toReturn)


def Legendary():
    """The legendary difficulty. Alpha-Beta pruning upto depth 4. Succumb, human."""
    ValidMoves = GetValidMoves()
    alpha = -LARGE
    beta = LARGE
    bestmove = ValidMoves[0]
    INITIAL_DEPTH = 4
    i = 0

    #Print statements for eval function.
    print 'Of board we got'
    (wsb,notwonlist) = WonSubBoards(state)
    
    print WhoseSubBoard(state,0,2)
    print 'Won sub-boards bonus: ' + str(wsb)
    print 'Almost won sub-boards bonus: ' + str(AlmostWonSubBoards(state,notwonlist))
 
    # Iterate over all valid moves, and set bestmove = argmax_move(bestmove_alpha,currmove_alpha)
    for move in ValidMoves:
        i += 1
        print 'Looked at %d moves' % (i,)
        newboard = copy.deepcopy(state)
        newboard[move[0]][move[1]][move[2]][move[3]] = turn       
        value = AlphaBeta(newboard,INITIAL_DEPTH,alpha,beta,False,[move[2],move[3]])
        if value > alpha:
            alpha = value
            bestmove = move
        del newboard

    # Evaluating a few other variables to print data for logging purposes
    newboard = copy.deepcopy(state)
    newboard[bestmove[0]][bestmove[1]][bestmove[2]][bestmove[3]] = turn       
    (wsb,notwonlist) = WonSubBoards(newboard)
    print 'Of board we send'
    print 'Won sub-boards bonus: ' + str(wsb)
    print 'Almost won sub-boards bonus: ' + str(AlmostWonSubBoards(newboard,notwonlist))
    del newboard

    # Preparing the move to return - [X,Y,x,y] where the first two are coords of the subboard within the board
    # and the next two are the coords of the tic tac toe square to be played, within the (X,Y) subboard.
    toReturn = str(bestmove[0]) + ',' + str(bestmove[1]) + ',' + str(bestmove[2]) + ',' + str(bestmove[3])
    return HttpResponse(toReturn)


# The view that renders the homepage
def home(request):
    return render_to_response('index.html', locals())


# The view to which the AJAX GET request is made
def getMove(request):

    # data being received:
    # turn - 1 is X, 2 is O
    # gameOver - true/false
    # state - state of board
    # wins - who's won each large grid?
    # nextBoard - the large grid in which the move is to be played (x,y)
    # X is from L to R, Y is from top to bottom.

    # Populating local data structures
    # with received data
    global turn
    global state
    global wins
    global nextboard
    global playanywhere
    turn = int(request.GET["turn"])
    if "nextBoard[]" not in request.GET.keys():
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

    # Choose bot based on difficulty setting
    diff = int(request.GET["difficulty"])
    if diff == 0:
        return Amateur()
    if diff == 1:
        return Professional()
    else:
        return Legendary()
