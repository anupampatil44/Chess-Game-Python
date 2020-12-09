# Driver File
# Handles user input and displays  the current game state information

import pygame as p
import numpy as np

# To be able to access the game state
import ChessEngine

# Size of the  chess board
WIDTH = HEIGHT  = 512

# Dimensions of the chess board ( 8 x 8 )
DIMENSION = 8

#  Side of a single square
SQ_SIZE = HEIGHT // DIMENSION

# Maximum frames per second
MAX_FPS = 15

IMAGES = {}

# Load the images
# Try to load it at once because loading images in a pygame is an expensive operation
# Initialize a global dictionary of images. This will be called exactly once in the main
def loadImages():
    pieces = np.array(["bR","bN","bB","bQ","bK","bp","wR","wN","wB","wQ","wK","wp"])
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

    # We can now access an image by using the dictionary IMAGES[piece_name]

# Main Driver and will handle user input and update graphics
# We have to make sure that we first draw the board and then the pieces
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    p.display.set_caption("Chess Game") #Window name
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.Gamestate()
    print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False    # Flag variable for when a move is made
    loadImages()        # Just once
    running = True
    sqSelected=() # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks=[] # keep track of the player clicks (two tuples [(6,4), (4,4)] to show the change in position of pieces
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False

            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected ==(row,col):  # User clicks the same square twice
                    sqSelected=()   # unselect
                    playerClicks=[] # reset player clicks
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)     # append for both first and second clicks
                # was that the user's second click
                if(len(playerClicks)==2):   # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () # reset  user clicks
                    playerClicks = []

            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # when z key is pressed
                    gs.undoMove()
                    moveMade = True

        if(moveMade):
            validMoves = gs.getValidMoves()
            moveMade = False

        piece, x, y = getSquareUnderMouse(gs.board)  # So that the square in which the mouse is get's highlighted
        drawGameState(screen, gs)
        drawSelector(screen, piece, x, y)
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all the graphics within a current game state
def drawGameState(screen, gs):
    drawBoard(screen)               # To draw the squares on the board
    # to add in piece highlighting or move suggestions, we have done the draiwng of the state in 2 different functions
    # highlighting is done below the piece and above the square
    drawPieces(screen, gs.board)    # To draw the pieces on top of the board

# Draw the squares
# The top-left square is always light
def drawBoard(screen):
    colors=[p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # All light  squares have an even parity and all the dark squares have an odd parity
            # So, we will choose the color of the sqaure based on the value for (r+c)%2
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces on the board using the current game states board variable
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!="--":     # not  an empty square
               screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getSquareUnderMouse(board):
    mouse_pos=p.Vector2(p.mouse.get_pos())
    x, y = [int(v // SQ_SIZE) for v in mouse_pos]
    try:
        if x>=0 and y>=0:
            return (board[x][y], x, y)
    except IndexError:  pass
    return None, None, None

def drawSelector(screen, piece, x, y):
    if piece != None:
        rect = (x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, (0,255,0,15), rect, 1)

if __name__ == "__main__":
    main()