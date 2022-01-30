from graphics import *
import math

class Square:
    def __init__(self):
        self.color = None
        self.piece = None
        self.pieceimg = None

def makeRect(corner, width, height):
    '''Return a new Rectangle given one corner Point and the dimensions.'''
    corner2 = corner.clone()

    corner2.move(width, height)
    return Rectangle(corner, corner2)

squareside = 50 # side length of board square

# square colors

squares = None
pieces  = None
pieceimgs = None
hls = None
hlcol = None
curcol = None
colors = None
win = None

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
    global squares, pieces, colors, hlcol, curcol, win, hls, pieceimgs
    squares   = [[None for y in range(height)] for x in range(width)] # 2d array of Rectangles
    pieces    = [[None for y in range(height)] for x in range(width)] # same, but for pieces (characters)
    pieceimgs = [[None for y in range(height)] for x in range(width)] # same, but for piece Images
    hls       = [[None for y in range(height)] for x in range(width)] # same, but for highlights (Rectangles)
    colors    = [color_rgb(240,114,114), color_rgb(241,241,201)] # black, white, highlight
    hlcol     = color_rgb(42,255,42)
    curcol    = 0

    win = GraphWin("board", squareside*width, squareside*height) # init window
    win.yUp() # y axis goes bottom to top

    for x in range(8):
        for y in range(8):
            curx = x*squareside
            cury = y*squareside
            r = makeRect(Point(curx, cury), squareside, squareside)
            squares[x][y] = r
            r.setFill(colors[curcol])
            r.setWidth(0)
            r.draw(win)

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
        

def hlsquare(file, rank):
    r = squares[file][rank]
    curhl = r.clone()
    curhl.setFill(hlcol)
    curhl.draw(win)
    hls[file][rank]

def unhlsquare(rank, file):
    h = hls[file][rank]
    if h != None:
        h.undraw()

def placepiece(file, rank, piece):
    delpiece(file, rank)
    cx = file*squareside + squareside/2
    cy = rank*squareside + squareside/2
    
    fn = 'sprites/' + spritemap[piece]

    curimg = Image(Point(cx, cy), fn)
    curimg.draw(win)
    pieceimgs[file][rank] = curimg

def delpiece(file, rank):
    p = pieceimgs[file][rank]
    if p != None:
        p.undraw()

def play(side): # get moves from alternating sides
    
