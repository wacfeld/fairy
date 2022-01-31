from graphics import *
import math

class Square:
    def __init__(self):
        self.rank = None
        self.file = None
        self.color = None # color_rgb
        self.rect = None # Rectangle
        self.hl = None # Rectangle
        self.piece = None # character
        self.pieceimg = None # Image

def makeRect(corner, width, height):
    '''Return a new Rectangle given one corner Point and the dimensions.'''
    corner2 = corner.clone()

    corner2.move(width, height)
    return Rectangle(corner, corner2)

squareside = 50 # side length of board square

board  = None
hlcol  = color_rgb(42,255,42) # highlight color
colors = [color_rgb(240,114,114), color_rgb(241,241,201)] # black, white
win    = None

# filenames of all piece sprites
spritemap = {}
spritemap['b'] = 'b-bishop.png'
spritemap['B'] = 'w-bishop.png'
spritemap['n'] = 'b-knight.png'
spritemap['N'] = 'w-knight.png'
spritemap['r'] = 'b-rook.png'
spritemap['R'] = 'w-rook.png'
spritemap['p'] = 'b-pawn.png'
spritemap['P'] = 'w-pawn.png'
spritemap['k'] = 'b-king.png'
spritemap['K'] = 'w-king.png'
spritemap['q'] = 'b-queen.png'
spritemap['Q'] = 'w-queen.png'

def createboard(width, height):
    # init some stuff
    global board, win
    board = [[Square() for i in range(height)] for j in range(width)]

    win = GraphWin("board", squareside*width, squareside*height) # init window
    win.yUp() # y axis goes bottom to top

    curcol = 0 # bottom left corner is black
    for x in range(width):
        for y in range(height):
            cursquare = board[x][y]

            curx = x*squareside
            cury = y*squareside

            # draw square
            r = makeRect(Point(curx, cury), squareside, squareside)
            r.setFill(colors[curcol])
            r.setWidth(0)
            r.draw(win)

            # update Square
            cursquare.rect = r
            cursquare.color = colors[curcol]
            cursquare.rank = y
            cursquare.file = x

            # toggle color
            curcol = (-1 * curcol) + 1
        curcol = (-1 * curcol) + 1
    # print(squares)
    
    # curhl = None
    # curimg = None
    # while True:
    #     p = win.getMouse()
    #     if curhl != None:
    #         curhl.undraw()
    #     print(p)
    #     # bottom left coords
    #     px = p.getX()
    #     py = p.getY()
    #     # center coords
    #     rank = math.floor(px/squareside)
    #     file = math.floor(py/squareside)
    #     cx = rank*squareside + squareside/2
    #     cy = file*squareside + squareside/2

    #     curimg = Image(Point(cx, cy), "sprites/b-bishop.png")
    #     curimg.draw(win)

#         r = squares[rank][file]
#         curhl = r.clone()
#         curhl.setFill(hlcol)
#         curhl.draw(win)
        

def hlsquare(s):
    curhl = s.rect.clone()
    curhl.setFill(hlcol)
    curhl.draw(win)
    if s.piece != None:
        s.pieceimg.undraw()
        s.pieceimg.draw(win)
    s.hl = curhl

def unhlsquare(s):
    if s.hl != None:
        s.hl.undraw()
    s.hl = None


def placepiece(s, piece):
    # clear that square first
    delpiece(s)

    # centered coords to place image
    file = s.file
    rank = s.rank
    cx = file*squareside + squareside/2
    cy = rank*squareside + squareside/2
    
    # image path
    fn = 'sprites/' + spritemap[piece]

    # draw image
    curimg = Image(Point(cx, cy), fn)
    curimg.draw(win)

    # update Square
    s.piece = piece
    s.pieceimg = curimg

def delpiece(s):
    if s.piece != None:
        s.pieceimg.undraw()
    s.piece = None
    s.pieceimg = None

def mouseSquare(m):
    x = m.getX()
    y = m.getY()
    file = math.floor(x/squareside)
    rank = math.floor(y/squareside)
    return board[file][rank]

def play(side): # get moves from alternating sides
    while True:
        s1 = mouseSquare(win.getMouse())
        if s1.piece == None:
            continue
        hlsquare(s1)
        s2 = mouseSquare(win.getMouse())
        p = s1.piece
        delpiece(s1)
        placepiece(s2, p)
        unhlsquare(s1)


        

