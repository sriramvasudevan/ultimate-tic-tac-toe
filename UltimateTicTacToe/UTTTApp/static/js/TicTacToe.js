function TicTacToe() {
    // drawing variables
    this.canvas = $("#board").get(0);
    this.context = this.canvas.getContext("2d");

    // standard line
    this.line = function(x0, y0, x1, y1) {
        this.context.beginPath();
        this.context.moveTo(x0,y0);
        this.context.lineTo(x1,y1);
        this.context.stroke();
        this.context.closePath();
    } 

    this.circle = function(x, y, r, fill) {
        this.context.beginPath();
        this.context.arc(x, y, r, 0, 2 * Math.PI, false);
        this.context.stroke();
        this.context.closePath();
    }

    // game variables
    this.turn = 1;
    this.gameOver = false;

    // the next board that the player has to play in, i.e. [0,0] = top left square
    this.nextBoard = null; //[1,1]; 
    this.useAI = false;
    this.useGambit = true;
    this.difficulty = 0;
    this.state = 	
        [
        [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]
            ];

    this.wins = [[0,0,0],[0,0,0],[0,0,0]];

    this.drawBoard = function() {
        var w = $("#board").width();
        var h = $("#board").height();

        // main board
        cxt = $("#board").get(0).getContext("2d");
        cxt.lineWidth = 3;
        this.line(0, h/3, w, h/3);
        this.line(0, 2/3*h, w, 2/3*h);
        this.line(w/3, 0, w/3, h);
        this.line(2/3*w, 0, 2/3*w, h);
        cxt.lineWidth = 1;

        // sub board
        this.drawSubBoard(0, 0); this.drawSubBoard(w/3, 0); this.drawSubBoard(2/3*w, 0);
        this.drawSubBoard(0, h/3); this.drawSubBoard(w/3, h/3); this.drawSubBoard(2/3*w, h/3);
        this.drawSubBoard(0, 2/3*h); this.drawSubBoard(w/3, 2/3*h); this.drawSubBoard(2/3*w, 2/3*h);

        // border
        cxt = $("#board").get(0).getContext("2d");
        cxt.lineWidth = 5;
        cxt.strokeRect(0,0,w,h);
        cxt.lineWidth = 2;
    }

    this.drawSubBoard = function(x, y) {
        var w = $("#board").width() / 3;
        var h = $("#board").height() / 3;

        this.line(x+8, (y+(h-16)/3)+8, x + w-8, y + ((h-16)/3)+8);
        this.line(x+8, (y+2/3*(h-16))+8, x + w-8, y + (2/3*(h-16))+8);
        this.line(x + ((w-16)/3)+8, y + 8, x + ((w-16)/3)+8, y + h-8);
        this.line(x + (2/3*(w-16))+8, y + 8, x + (2/3*(w-16))+8, y + h-8);


        // this.line(x+8, y + 8, x + w-8, y + 8);
        // this.line(x+8, y + 8, x + 8, y + h-8);
        // this.line(x+8, y + h-8, x + w-8, y + h-8);
        // this.line(x+w-8, y + 8, x + w-8, y + h-8);
    }

    this.isWon = function(subboard_coords) {
        return this.wins[subboard_coords[0]][subboard_coords[1]];
    }

    this.getCurrentSubBoard = function() {
        return this.state[this.nextBoard[0]][this.nextBoard[1]];
    }

    this.isSubBoardFull = function(board) {
        if(board == null) {
            return false;
        }
        return board[0][0] != 0 && board[1][0] != 0 && board[2][0] != 0
            && board[0][1] != 0 && board[1][1] != 0 && board[2][1] != 0
            && board[0][2] != 0 && board[1][2] != 0 && board[2][2] != 0
    }

    this.switchTurns = function() {
        if(this.turn == 2) {
            this.turn = 1;
            $("#turn").html("X's Turn.");
        } else if(this.turn == 1) {
            this.turn = 2;
            $("#turn").html("O's Turn.");
        }
    }

    this.clickedValidBoard = function(x, y) {
        if(this.nextBoard == null) {
            return true;
        }
        var w = $("#board").width();
        var h = $("#board").height();

        if(x > this.nextBoard[0]*w/3 
                && x < (this.nextBoard[0]+1)*w/3
                && y > this.nextBoard[1]*h/3 
                && y < (this.nextBoard[1]+1)*h/3) {
                    return true;
                }
        return false;
    }

    this.getLocalCoord = function(x, y) {
        var w = $("#board").width() / 3;
        var h = $("#board").height() / 3;
        if(this.nextBoard == null) {
            this.nextBoard = [
                parseInt(x / w),
                parseInt(y / h)
                    ];
        }

        var x0 = this.nextBoard[0]*w;
        var y0 = this.nextBoard[1]*h;
        var lx = parseInt((x-x0) / w * 3);
        var ly = parseInt((y-y0) / h * 3);
        return [lx, ly];
    }

    this.clickedEmptySpace = function(x, y) {
        var lxy = this.getLocalCoord(x, y);
        var lx = lxy[0];
        var ly = lxy[1];

        if(this.state[this.nextBoard[0]][this.nextBoard[1]][lx][ly] == 0) {
            return true;
        }
        return false;
    }

    this.drawO = function(x, y) {
        // var w = ($("#board").width()/3-16)/3;
        // var h = ($("#board").height()/3-16)/3;

        // cxt = $("#board").get(0).getContext("2d");
        // cxt.strokeStyle = "#CE0000";
        // cxt.fillStyle = "#CE0000";
        // cxt.fillRect(x+12, y+12, w-8, h-8);


        var w = ($("#board").width()/3-16)/3;

        cxt = $("#board").get(0).getContext("2d");
        cxt.strokeStyle = "#CE0000";

        this.circle(x + w/2 + 8, y + w/2 + 8, w/2 - 8, false, 5);
    }

    this.drawX = function(x, y) {
        var w = ($("#board").width()/3-16)/3;
        var h = ($("#board").height()/3-16)/3;

        cxt = $("#board").get(0).getContext("2d");
        cxt.strokeStyle = "#000063";
        // cxt.fillStyle = "#000063";
        // cxt.fillRect(x+12, y+12, w-8, h-8);

        this.line(x+16, y+16, x+w, y+h);
        this.line(x+w, y+16, x+16, y+h);
    }

    this.go = function(lx, ly) {
        this.state[this.nextBoard[0]][this.nextBoard[1]][lx][ly] = this.turn;
        var w = $("#board").width() / 3;
        var h = $("#board").height() / 3;

        var dX = this.nextBoard[0] * w + lx * (w-16) / 3;
        var dY = this.nextBoard[1] * h + ly * (h-16) / 3;
        if(this.turn == 2) {
            this.drawO(dX, dY);
        } else if(this.turn == 1) {
            this.drawX(dX, dY);
        }
        this.handleWins(this.nextBoard[0], this.nextBoard[1], 1);
        this.handleWins(this.nextBoard[0], this.nextBoard[1], 2);
        this.nextBoard = [lx, ly];
    }


    this.highlightBoard = function() {
        var w = $("#board").width() / 3;
        var h = $("#board").height() / 3;
        if(this.nextBoard == null) {
            $("#board").css("background-repeat", "repeat");
            $("#board").css("background-position", "0px 0px");
        } else {
            var pos = (this.nextBoard[0]*w) + "px " + (this.nextBoard[1]*h) + "px";
            $("#board").css("background-repeat", "no-repeat");
            $("#board").css("background-position", pos);
        }
    }

    this.handleWins = function(x, y, turn) {
        var w = $("#board").width() / 3;
        var h = $("#board").height() / 3;
        var dX = this.nextBoard[0] * w;
        var dY = this.nextBoard[1] * h;

        var board = this.state[x][y];
        if(this.wins[x][y] > 0) {
            return;
        }

        // local wins
        // horizontal
        if(turn==1) {
            cxt = $("#board").get(0).getContext("2d");
            cxt.strokeStyle = "#000063";
        }
        else if(turn==2) {
            cxt = $("#board").get(0).getContext("2d");
            cxt.strokeStyle = "#CE0000";
        }
        if(this.wins[x][y]==0 && board[0][0] == turn && board[1][0] == turn && board[2][0] == turn) {
            this.line(dX+12, dY + (h/3-8)/2+8, dX + w-12, dY + (h/3-8)/2+8);
            this.wins[x][y] = turn;
        }
        if(this.wins[x][y]==0 && board[0][1] == turn && board[1][1] == turn && board[2][1] == turn) {
            this.line(dX+12, dY + ((h/3-8)/2+h/3-4)+8, dX + w-12, dY + ((h/3-8)/2+h/3-4)+8);
            this.wins[x][y] = turn;
        }
        if(this.wins[x][y]==0 && board[0][2] == turn && board[1][2] == turn && board[2][2] == turn) {
            this.line(dX+12, dY + ((h/3-8)/2+2/3*h-10)+8, dX + w-12, dY + ((h/3-8)/2+2/3*h-10)+8);
            this.wins[x][y] = turn;
        }
        // vertical
        if(this.wins[x][y]==0 && board[0][0] == turn && board[0][1] == turn && board[0][2] == turn) {
            this.line(dX+(w/3-8)/2+9, dY+12, dX+(w/3-8)/2+9, dY+h-12);
            this.wins[x][y] = turn;
        }
        if(this.wins[x][y]==0 && board[1][0] == turn && board[1][1] == turn && board[1][2] == turn) {
            this.line(dX+((w/3-8)/2+(w/3-4))+8, dY+12, dX+((w/3-8)/2+(w/3-4))+8, dY+h-12);
            this.wins[x][y] = turn;
        }
        if(this.wins[x][y]==0 && board[2][0] == turn && board[2][1] == turn && board[2][2] == turn) {
            this.line(dX+((w/3-8)/2+2/3*w-8)+7, dY+12, dX+((w/3-8)/2+2/3*w-8)+7, dY+h-12);
            this.wins[x][y] = turn;
        }
        // diagonal
        if(this.wins[x][y]==0 && board[0][0] == turn && board[1][1] == turn && board[2][2] == turn) {
            this.line(dX+12, dY+12, dX+w-12, dY+h-12);
            this.wins[x][y] = turn;
        }
        if(this.wins[x][y]==0 && board[2][0] == turn && board[1][1] == turn && board[0][2] == turn) {
            this.line(dX+12, dY+h-12, dX+w-12, dY+12);
            this.wins[x][y] = turn;
        }

        if(this.wins[x][y] > 0) {
            $("#score" + turn).html(parseInt($("#score" + turn).html()) + 1);
        }

        // global wins
        // horizontal
        if(this.hasWon(turn)) {
            if(turn == 2) {
                $("#turn").html("O Wins!");
                this.gameOver = true;
            } else if(turn == 1) {
                $("#turn").html("X Wins!");
                this.gameOver = true;
            }
        }
    }

    this.hasWon = function(turn) {
        if((this.wins[0][0] == turn && this.wins[1][0] == turn && this.wins[2][0] == turn)
                || (this.wins[0][1] == turn && this.wins[1][1] == turn && this.wins[2][1] == turn) 
                || (this.wins[0][2] == turn && this.wins[1][2] == turn && this.wins[2][2] == turn)
                || (this.wins[0][0] == turn && this.wins[0][1] == turn && this.wins[0][2] == turn)
                || (this.wins[1][0] == turn && this.wins[1][1] == turn && this.wins[1][2] == turn)
                || (this.wins[2][0] == turn && this.wins[2][1] == turn && this.wins[2][2] == turn) 
                || (this.wins[0][0] == turn && this.wins[1][1] == turn && this.wins[2][2] == turn)
                || (this.wins[2][0] == turn && this.wins[1][1] == turn && this.wins[0][2] == turn)) {
                    return true;
                }
        return false;
    }

    this.move = function(x, y) {
        if(this.clickedValidBoard(x, y)) {
            if(this.clickedEmptySpace(x, y)) {
                var lxy = this.getLocalCoord(x, y);
                var lx = lxy[0];
                var ly = lxy[1];
                this.go(lx, ly);
                return true;
            } else {
                $("#msg").html("That space is already been played!");
            }
        } else {
            $("#msg").html("Make a move in the highlighted board.");
        }
        return false;
    } 

    this.toggleGambit = function() {
        this.useGambit = !this.useGambit;
        if(this.useGambit) {
            $("#toggle_gambit").attr("value", "Gambit Enabled");
        } else {
            $("#toggle_gambit").attr("value", "Gambit Disabled");
        }
    }

    this.toggleAI = function() {
        this.useAI = !this.useAI;
        if(this.useAI) {
            $("#toggle_ai").attr("value", "1 vs AI");
        } else {
            $("#toggle_ai").attr("value", "1 vs 1");
        }
    }

    this.toggleDifficulty = function() {
        if(this.difficulty==0) {
            $("#toggle_difficulty").attr("value", "Professional");
            this.difficulty = 1;
        } else if(this.difficulty==1) {
            $("#toggle_difficulty").attr("value", "Legendary");
            this.difficulty = 2;
        }
        else {
            $("#toggle_difficulty").attr("value", "Amateur");
            this.difficulty = 0;
        }
    }

    this.solve = function(nextBoard) {
        var retval = [0,0,1,1];
        $.ajax({
          url: "getmove",
          data: {
              turn: this.turn,
              gameOver: this.gameOver,
              state: this.state,
              wins: this.wins,
              difficulty: this.difficulty,
              nextBoard: this.nextBoard
          },
          async: false,
          cache: false
        }).done(function(result) {
            result = result.split(",");
            for(var i=0; i<result.length; i++) {
                retval[i] = parseInt(result[i]);
            }
        });
        return retval;
    }

    this.aiGo = function() {
        var move = this.solve(this.nextBoard);
        this.nextBoard = [move[0], move[1]];
        this.go(move[2], move[3]);

        if(!this.gameOver) {
            $("#msg").html("&nbsp;");
        }
        this.switchTurns();		
        //account for all filled subboards
        if(this.isSubBoardFull(this.state[0][0])&&this.isSubBoardFull(this.state[0][1])&&this.isSubBoardFull(this.state[0][2])&&this.isSubBoardFull(this.state[1][0])&&this.isSubBoardFull(this.state[1][1])&&this.isSubBoardFull(this.state[1][2])&&this.isSubBoardFull(this.state[2][0])&&this.isSubBoardFull(this.state[2][1])&&this.isSubBoardFull(this.state[2][2])) {
            if(parseInt($("#score1").html())>parseInt($("#score2").html())) {
                $("#turn").html("X Wins!");
            }
            else {
                $("#turn").html("O Wins!");
            }
            this.gameOver = true;
        }
        // account for filled squares
        if(this.useGambit) {
            if(this.nextBoard != null && this.isSubBoardFull(this.getCurrentSubBoard())) {
                this.nextBoard = null;
            }
        }
        else {
            if(this.nextBoard != null && (this.isSubBoardFull(this.getCurrentSubBoard())||this.isWon(this.nextBoard))) {
                this.nextBoard = null;
            }
        }
        this.highlightBoard();
    }

    this.handleInput = function(x, y) {
        if(!this.gameOver) {
            var moved = this.move(x, y);
            if(moved) {
                //account for all filled subboards
                if(this.isSubBoardFull(this.state[0][0])&&this.isSubBoardFull(this.state[0][1])&&this.isSubBoardFull(this.state[0][2])&&this.isSubBoardFull(this.state[1][0])&&this.isSubBoardFull(this.state[1][1])&&this.isSubBoardFull(this.state[1][2])&&this.isSubBoardFull(this.state[2][0])&&this.isSubBoardFull(this.state[2][1])&&this.isSubBoardFull(this.state[2][2])) {
                    if(parseInt($("#score1").html())>parseInt($("#score2").html())) {
                        $("#turn").html("X Wins!");
                    }
                    else {
                        $("#turn").html("O Wins!");
                    }
                    this.gameOver = true;
                }
                // account for filled squares
                // the isWon() gets rid of the gambit possibility,
                // a version of the game that allows X to play perfectly.
                if(this.useGambit) {
                    if(this.nextBoard != null && this.isSubBoardFull(this.getCurrentSubBoard())) {
                        this.nextBoard = null;
                    }
                }
                else {
                    if(this.nextBoard != null && (this.isSubBoardFull(this.getCurrentSubBoard())||this.isWon(this.nextBoard))) {
                        this.nextBoard = null;
                    }
                }
                this.highlightBoard();
                if(!this.gameOver) {
                    $("#msg").html("&nbsp;");
                    this.switchTurns();
                }
                if(this.useAI && !this.gameOver) {
                    this.aiGo();
                }
            }
        }
    }

    this.handleClick = function(e) {
        var offset = $("#board").offset();
        var x = e.clientX - offset.left + $(window).scrollLeft();
        var y = e.clientY - offset.top + $(window).scrollTop();

        this.handleInput(x, y);
    }	

    $("#msg").html("Start by clicking anywhere.");

    // handle click/touch events
    var board = this;
    $("#board").click(function(e) {
        board.handleClick(e);
    });
    $("#board").bind("touchstart", function(e) {
        var targetEvent =  e.touches.item(0);
        board.handleClick(targetEvent);
    });
}
