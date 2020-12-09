# For storing all information about the currrent state of a chess game
# Also be responsible for determining the valid moevs at the current state
# It will also keep a move log

import numpy as np;

class Gamestate():
    def __init__(self):
        # Board is an 8x8 array and each element has 2 characters -  the color of the piece and the second character represents the type of the piece
        # color: b, w
        # piece: K, Q, B, N, R, p
        # -- represents empty place with no pieces
        # Using 2d array to store each place
        self.board = np.array([["bR","bN","bB","bQ","bK","bB","bN","bR"],
                               ["bp","bp","bp","bp","bp","bp","bp","bp"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["wp","wp","wp","wp","wp","wp","wp","wp"],
                               ["wR","wN","wB","wQ","wK","wB","wN","wR"]]).reshape(8,8)
        self.whiteToMove = True
        self.moveLog = []

    # takes a move as a parameter and executes it. Does not work for castling, pawn promotion and en-passant
    def makeMove(self, move):
        if(self.board[move.startRow][move.startCol]=="--"):
            return
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)   # log the move so that we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove  = not self.whiteToMove    # switch turns back

    def getKingPosition(self, whiteToMove):
        if(whiteToMove):
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if(self.board[r][c]=="wK"):
                        return (r,c)
        else:
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if(self.board[r][c]=="bK"):
                        return (r,c)

    # All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # All moves without considering checks
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):            # number of rows
            for c in range(len(self.board[0])):     # number of columns
                turn = self.board[r][c][0]
                if(turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece=='p':
                        self.getPawnMoves(r, c, moves)
                    elif piece=='R':
                        self.getRookMoves(r, c, moves)
                    elif piece=='N':
                        self.getKnightMoves(r, c, moves)
                    elif piece=='B':
                        self.getBishopMoves(r, c, moves)
                    elif piece=='Q':
                        self.getQueenMoves(r,  c, moves)
                    elif piece=='K':
                        self.getKingMoves(r, c, moves)
        return moves

    # get all the pawn moves for the pawn located at row, column and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if(self.whiteToMove):   # white pawn moves
            if(self.board[r-1][c]=="--"): # 1 square pawn advance
                self.makeMove(Move((r, c), (r - 1, c), self.board))
                if (len(self.getChecks(self.getKingPosition(self.whiteToMove))) == 0):
                    self.undoMove()
                    moves.append(Move((r, c), (r - 1, c), self.board))
                else:
                    self.undoMove()
                if(self.board[r-2][c]=="--" and r==6):
                    self.makeMove(Move((r, c), (r - 2, c), self.board))
                    if(len(self.getChecks(self.getKingPosition(self.whiteToMove)))==0):
                        self.undoMove()
                        moves.append(Move((r, c), (r - 2, c), self.board))
                    else:
                        self.undoMove()
            if(self.board[r-1][c-1]!="--"):
                self.makeMove(Move((r, c), (r - 1, c - 1), self.board))
                if (len(self.getChecks(self.getKingPosition(self.whiteToMove))) == 0):
                    self.undoMove()
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                else:
                    self.undoMove()
            if (c<7 and self.board[r-1][c+1] != "--"):
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:                   # black pawn moves
            if (self.board[r + 1][c] == "--"):  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if (self.board[r + 2][c] == "--" and r == 1):
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if (self.board[r + 1][c - 1] != "--"):
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if (c < 7 and self.board[r + 1][c + 1] != "--"):
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    # get all the rook moves for the pawn located at row, column and add these moves to the list
    def getRookMoves(self, r, c, moves):
        # forward
        i = 1
        while(r + i < 8):
            if(self.board[r+i][c]=='--'):
                moves.append(Move((r,c),(r+i,c),self.board))
            elif (self.board[r+i][c][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r+i, c), self.board))
                break
            else:
                break
            i+=1

        # backward
        i = 1
        while (r - i >= 0):
            if (self.board[r-i][c] == '--'):
                moves.append(Move((r, c), (r - i, c), self.board))
            elif(self.board[r-i][c][0]!=self.board[r][c][0]):
                moves.append(Move((r, c), (r - i, c), self.board))
                break
            else:
                break
            i += 1

        # left
        i = 1
        while (c - i >= 0):
            if (self.board[r][c-i] == '--'):
                moves.append(Move((r, c), (r, c-i), self.board))
            elif (self.board[r][c-i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r, c-i), self.board))
                break
            else:
                break
            i += 1

        # right
        i = 1
        while (c + i < 8):
            if (self.board[r][c+i] == '--'):
                moves.append(Move((r, c), (r, c+i), self.board))
            elif (self.board[r][c+i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r, c+i), self.board))
                break
            else:
                break
            i += 1

    # get all the knight moves for the pawn located at row, column and add these moves to the list
    def getKnightMoves(self, r, c, moves):
        # forward_left
        if(r+2<8 and c-1>=0):
            if(self.board[r+2][c-1]=="--" or self.board[r+2][c-1][0]!=self.board[r][c][0]):
                moves.append(Move((r,c),(r+2,c-1),self.board))

        # forward_right
        if(r+2<8 and c+1<8):
            if(self.board[r+2][c+1]=="--" or self.board[r+2][c+1][0]!=self.board[r][c][0]):
                moves.append(Move((r,c),(r+2,c+1),self.board))

        # backward_left
        if(r-2>=0 and c-1>=0):
            if(self.board[r-2][c-1]=="--" or self.board[r-2][c-1][0]!=self.board[r][c][0]):
                moves.append(Move((r,c),(r-2,c-1),self.board))

        # backward right
        if(r-2>=0 and c+1<8):
            if(self.board[r-2][c+1]=="--" or self.board[r-2][c+1][0]!=self.board[r][c][0]):
                moves.append(Move((r,c),(r-2,c+1),self.board))

        # leftward forward
        if (r + 1 < 8 and c - 2 >= 0):
            if (self.board[r + 1][c - 2] == "--" or self.board[r+1][c-2][0]!=self.board[r][c][0]):
                moves.append(Move((r, c), (r + 1, c - 2), self.board))

        # rightward forward
        if (r + 1 < 8 and c + 2 < 8):
            if (self.board[r + 1][c + 2] == "--" or self.board[r+1][c+2][0]!=self.board[r][c][0]):
                moves.append(Move((r, c), (r + 1, c + 2), self.board))

        # leftward backward
        if (r - 1 >=0 and c - 2 >= 0):
            if (self.board[r - 1][c - 2] == "--" or self.board[r-1][c-2][0]!=self.board[r][c][0]):
                moves.append(Move((r, c), (r - 1, c - 2), self.board))

        # rightward backward
        if (r - 1 >=0 and c + 2 < 8):
            if (self.board[r - 1][c + 2] == "--" or self.board[r-1][c+1][0]!=self.board[r][c][0]):
                moves.append(Move((r, c), (r - 1, c + 2), self.board))

    # get all the bishop moves for the pawn located at row, column and add these moves to the list
    def getBishopMoves(self, r, c, moves):

        # forward_left
        i = 1
        while (r + i < 8 and c - i >= 0):
            if (self.board[r + i][c - i] == '--'):
                moves.append(Move((r, c), (r + i, c - i), self.board))
            elif (self.board[r + i][c - i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r + i, c - i), self.board))
                break
            else:
                break
            i += 1

        # forward_right
        i = 1
        while (r + i < 8 and c + i <8):
            if (self.board[r + i][c + i] == '--'):
                moves.append(Move((r, c), (r + i, c + i), self.board))
            elif (self.board[r + i][c + i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r + i, c + i), self.board))
                break
            else:
                break
            i += 1

        # backward_left
        i = 1
        while (r-i>=0 and c - i >= 0):
            if (self.board[r-i][c - i] == '--'):
                moves.append(Move((r, c), (r-i, c - i), self.board))
            elif (self.board[r-i][c - i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r-i, c - i), self.board))
                break
            else:
                break
            i += 1

        # backward_right
        i = 1
        while (r - i >=0 and c + i < 8):
            if (self.board[r - i][c + i] == '--'):
                moves.append(Move((r, c), (r - i, c + i), self.board))
            elif (self.board[r - i][c + i][0] != self.board[r][c][0]):
                moves.append(Move((r, c), (r - i, c + i), self.board))
                break
            else:
                break
            i += 1

    # get all the queen moves for the queen located at row, column and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    # get all the king moves for the king located at row, column and add these moves to the list
    def getKingMoves(self, r, c, moves):

        # forward
        if (r+1<8):
            if(self.board[r + 1][c] == "--" or self.board[r + 1][c][0] != self.board[r][c][0]):
                if(len(self.getChecks(r+1,c))==0):
                    moves.append(Move((r, c), (r + 1, c), self.board))

        # forward_right
        if (r+1<8  and  c+1<8):
            if(self.board[r + 1][c+1] == "--" or self.board[r + 1][c+1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r + 1, c+1)) == 0):
                    moves.append(Move((r, c), (r + 1, c+1), self.board))

        # forward_left
        if (r+1<8 and c-1>=0):
            if(self.board[r + 1][c-1] == "--" or self.board[r + 1][c-1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r + 1, c-1)) == 0):
                    moves.append(Move((r, c), (r + 1, c-1), self.board))

        # backward
        if (r-1>=0):
            if(self.board[r - 1][c] == "--" or self.board[r - 1][c][0] != self.board[r][c][0]):
                if (len(self.getChecks(r - 1, c)) == 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))

        # backward_right
        if (r-1>=0 and c+1<8):
            if(self.board[r - 1][c+1] == "--" or self.board[r - 1][c+1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r - 1, c+1)) == 0):
                    moves.append(Move((r, c), (r - 1, c+1), self.board))

        # backward_left
        if (r-1>=0 and c-1>=0):
            if(self.board[r - 1][c-1] == "--" or self.board[r - 1][c-1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r - 1, c-1)) == 0):
                    moves.append(Move((r, c), (r - 1, c-1), self.board))

        # right
        if (c+1<8):
            if(self.board[r][c+1] == "--" or self.board[r][c+1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r, c+1)) == 0):
                    moves.append(Move((r, c), (r, c+1), self.board))

        # left
        if (c-1>=0):
            if(self.board[r][c-1] == "--" or self.board[r][c-1][0] != self.board[r][c][0]):
                if (len(self.getChecks(r, c-1)) == 0):
                    moves.append(Move((r, c), (r, c-1), self.board))

    def getChecks(self, r, c):
        kMove=[]

        # backward_left
        i=1
        while(r-i>=0 and c-i>=0):
            if((self.board[r-i][c-i][1]=="B" or self.board[r-i][c-i][1]=="Q") and self.board[r][c][0]!=self.board[r-i][c-i][0]):
                kMove.append(Move((r,c),(r-i,c-i),self.board))
            elif(self.board[r-i][c-i]=="--"):
                pass
            else:
                break
            i+=1

        # backward_right
        i = 1
        while (r - i >= 0 and c + i < 8):
            if ((self.board[r - i][c + i][1] == "B" or self.board[r - i][c + i][1] == "Q") and self.board[r][c][0] != self.board[r - i][c + i][0]):
                kMove.append(Move((r, c), (r - i, c + i), self.board))
            elif (self.board[r - i][c + i] == "--"):
                pass
            else:
                break
            i += 1

        # forward_left
        i = 1
        while (r + i < 8 and c - i >=0):
            if ((self.board[r + i][c - i][1] == "B" or self.board[r + i][c - i][1] == "Q") and self.board[r][c][0] != self.board[r + i][c - i][0]):
                kMove.append(Move((r, c), (r + i, c - i), self.board))
            elif (self.board[r + i][c - i] == "--"):
                pass
            else:
                break
            i += 1

        # forward_right
        i = 1
        while (r + i < 8 and c + i < 8):
            if ((self.board[r + i][c + i][1] == "B" or self.board[r + i][c + i][1] == "Q") and self.board[r][c][0] != self.board[r + i][c + i][0]):
                kMove.append(Move((r, c), (r + i, c + i), self.board))
            elif (self.board[r + i][c + i] == "--"):
                pass
            else:
                break
            i += 1

        # forward
        i = 1
        while (r + i < 8):
            if ((self.board[r + i][c][1] == "R" or self.board[r + i][c][1] == "Q") and self.board[r][c][0] != self.board[r + i][c][0]):
                kMove.append(Move((r, c), (r + i, c), self.board))
            elif (self.board[r + i][c] == "--"):
                pass
            else:
                break
            i += 1

        # backward
        i = 1
        while (r - i >= 0):
            if ((self.board[r - i][c][1] == "R" or self.board[r - i][c][1] == "Q") and self.board[r][c][0] != self.board[r - i][c][0]):
                kMove.append(Move((r, c), (r - i, c), self.board))
            elif (self.board[r - i][c] == "--"):
                pass
            else:
                break
            i += 1

        # left
        i = 1
        while (c - i >= 0):
            if ((self.board[r][c-i][1] == "R" or self.board[r][c-i][1] == "Q") and self.board[r][c][0] != self.board[r][c-i][0]):
                kMove.append(Move((r, c), (r, c-i), self.board))
            elif (self.board[r][c - i] == "--"):
                pass
            else:
                break
            i += 1

        # right
        i = 1
        while (c + i < 8):
            if ((self.board[r][c+i][1] == "R" or self.board[r][c+i][1] == "Q") and self.board[r][c][0] != self.board[r][c+i][0]):
                kMove.append(Move((r, c), (r, c+i), self.board))
            elif (self.board[r][c + i] == "--"):
                pass
            else:
                break
            i += 1

        # forward_left k
        if(r+2<8 and c-1>=0):
            if(self.board[r+2][c-1][1]=="N" and self.board[r][c][0]!=self.board[r+2][c-1][0]):
                kMove.append(Move((r, c), (r+2, c-1), self.board))

        # leftward_forward k
        if (r + 1 < 8 and c - 2 >= 0):
            if (self.board[r + 1][c - 2][1] == "N" and self.board[r][c][0] != self.board[r + 1][c - 2][0]):
                kMove.append(Move((r, c), (r + 1, c - 2), self.board))

        # forward_right k
        if (r + 2 < 8 and c + 1 < 8):
            if (self.board[r + 2][c + 1][1] == "N" and self.board[r][c][0] != self.board[r + 2][c + 1][0]):
                kMove.append(Move((r, c), (r + 2, c + 1), self.board))

        # rightward_forward
        if (r + 1 < 8 and c + 2 < 8):
            if (self.board[r + 1][c + 2][1] == "N" and self.board[r][c][0] != self.board[r + 1][c + 2][0]):
                kMove.append(Move((r, c), (r + 1, c + 2), self.board))

        # backward_left k
        if (r - 2 >= 0 and c - 1 >= 0):
            if (self.board[r - 2][c - 1][1] == "N" and self.board[r][c][0] != self.board[r - 2][c - 1][0]):
                kMove.append(Move((r, c), (r - 2, c - 1), self.board))

        # leftward_backward
        if (r - 1 >=0 and c - 2 >= 0):
            if (self.board[r - 1][c - 2][1] == "N" and self.board[r][c][0] != self.board[r - 1][c - 2][0]):
                kMove.append(Move((r, c), (r - 1, c - 2), self.board))

        # backward_right k
        if (r - 2 >=0 and c + 1 < 8):
            if (self.board[r - 2][c + 1][1] == "N" and self.board[r][c][0] != self.board[r - 2][c + 1][0]):
                kMove.append(Move((r, c), (r - 2, c + 1), self.board))

        # rightward_backward
        if (r - 1 >=0 and c + 2 < 8):
            if (self.board[r - 1][c + 2][1] == "N" and self.board[r][c][0] != self.board[r - 1][c + 2][0]):
                kMove.append(Move((r, c), (r - 1, c + 2), self.board))

        # forward_left p
        if(r+1<8 and c-1>=0):
            if (self.board[r + 1][c - 1][1] == "p" and self.board[r][c][0] != self.board[r + 1][c - 1][0]):
                kMove.append(Move((r, c), (r + 1, c - 1), self.board))

        # forward_right p
        if (r + 1 < 8 and c + 1 < 8):
            if (self.board[r + 1][c + 1][1] == "p" and self.board[r][c][0] != self.board[r + 1][c + 1][0]):
                kMove.append(Move((r, c), (r + 1, c + 1), self.board))

        # backward_left p
        if (r - 1 >= 0 and c - 1 >= 0):
            if (self.board[r - 1][c - 1][1] == "p" and self.board[r][c][0] != self.board[r - 1][c - 1][0]):
                kMove.append(Move((r, c), (r - 1, c - 1), self.board))

        # backward_right
        if (r - 1 >= 0 and c + 1 < 8):
            if (self.board[r - 1][c + 1][1] == "p" and self.board[r][c][0] != self.board[r - 1][c + 1][0]):
                kMove.append(Move((r, c), (r - 1, c + 1), self.board))

        return kMove

class Move():

    # maps keys to values
    # key : value
    # For names of rows and columns used in chess notation
    ranksToRows =  {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    # Way of reversing a dictionary, key to value and value to key
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board):
        # a move in chess has a start square and an end square
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
