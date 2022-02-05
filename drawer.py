from graphics import *
from objects import *

import math

def makeRect(corner, width, height):
    '''Return a new Rectangle given one corner Point and the dimensions.'''
    corner2 = corner.clone()

    corner2.move(width, height)
    return Rectangle(corner, corner2)

squareside = 50 # side length of board square

board  = None
hlcol  = color_rgb(42,255,42) # highlight color
colors = [color_rgb(240,114,114), color_rgb(241,241,201)] # pink, white
# colors = [color_rgb(93,93,93), color_rgb(241,241,201)] # grey, white
# colors = [color_rgb(255,165,0), color_rgb(241,241,201)] # orange, white
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

# create board, draw
def init(width, height):
    # init some stuff
    global board, win
    board = Board()

    # Board.board can hold both characters and Squares as needed, for graphics and backend
    board.board = [[Square() for i in range(height)] for j in range(width)]

    win = GraphWin("board", squareside*width, squareside*height) # init window
    win.yUp() # y axis goes bottom to top

    curcol = 0 # bottom left corner is black
    for x in range(width):
        for y in range(height):
            cursquare = board.get((x,y))

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
        
# consumes Board, updates the GUI board as needed
def update(newboard):
    width = newboard.width
    height = newboard.height
    locs = [(x,y) for x in range(width) for y in range(height)]

    for l in locs:
        # keep in mind the different "types" of these boards, one holds Squares (which hold characters), one holds characters
        s = board.get(l)
        newpiece = newboard.get(l)
        if newpiece != None and newpiece.name == s.piece: # if same, don't need to update this square
            continue
        # otherwise, update
        placepiece(s, newpiece)

def hlloc(l):
    hlsquare(board.get(l))

def hlsquare(s):
    if s.hl != None: # already highlighted, ignore
        return
    curhl = s.rect.clone()
    curhl.setFill(hlcol)
    curhl.draw(win)
    if s.piece != None:
        s.pieceimg.undraw()
        s.pieceimg.draw(win)
    s.hl = curhl

def unhlloc(l):
    unhlsquare(board.get(l))

def unhlsquare(s):
    if s.hl != None:
        s.hl.undraw()
    s.hl = None

def locplacepiece(l, piece):
    placepiece(board.get(l), piece)

def placepiece(s, piece):
    # clear that square first
    delpiece(s)

    if piece == None: # when told to place None, simply clear that square
        return

    # centered coords to place image
    file = s.file
    rank = s.rank
    cx = file*squareside + squareside/2
    cy = rank*squareside + squareside/2
    
    # image path
    fn = 'sprites/' + spritemap[piece.name]

    # draw image
    curimg = Image(Point(cx, cy), fn)
    curimg.draw(win)

    # update Square
    s.piece = piece.name
    s.pieceimg = curimg

def locdelpiece(l):
    delpiece(board.get(l))

def delpiece(s):
    if s.piece != None:
        s.pieceimg.undraw()
    s.piece = None
    s.pieceimg = None

def mousesquare(m):
    x = m.getX()
    y = m.getY()
    file = math.floor(x/squareside)
    rank = math.floor(y/squareside)
    return board.get((file,rank))

def getmousesquare():
    return mousesquare(win.getMouse())
