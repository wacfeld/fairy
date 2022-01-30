from graphics import *
import math

'''
make a chessboard
figure out where clicks land
put pieces on the chessboard
move pieces on the chessboard
'''

def makeRect(corner, width, height):
    '''Return a new Rectangle given one corner Point and the dimensions.'''
    corner2 = corner.clone()

    corner2.move(width, height)
    return Rectangle(corner, corner2)

def main():
    squareside = 50 # side length of board square

    # square colors
    colors = [color_rgb(240,114,114), color_rgb(241,241,201)] # black, white, highlight
    hlcol = color_rgb(42,255,42)
    curcol = 0

    # dimensions of board
    width = 8
    height = 8

    win = GraphWin("board", squareside*width, squareside*height) # init window
    win.yUp() # y axis goes bottom to top

    squares = [[None for y in range(height)] for x in range(width)] # 2d array

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

    print(squares)
    
    curhl = None
    while True:
        p = win.getMouse()
        if curhl != None:
            curhl.undraw()
        print(p)
        px = p.getX()
        py = p.getY()
        rank = math.floor(px/squareside)
        file = math.floor(py/squareside)
        r = squares[rank][file]
        curhl = r.clone()
        curhl.setFill(hlcol)
        curhl.draw(win)
        

if __name__ == '__main__':
    main()
