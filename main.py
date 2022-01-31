import drawer
import moves
from objects import *

'''
- [x] make a chessboard
- [x] figure out where clicks land
- [x] put pieces on the chessboard
- [x] FEN -> board
- [ ] board -> FEN
- [x] move pieces on the chessboard
- [ ] get legal moves on chessboard, based on arbitrary fairy chess move properties
- [ ] determine check and checkmate
- [ ] make an engine that's good
- [ ] make object oriented
- [ ] make readfen() call drawer.update()
'''


height = 8
width = 8


# read FEN, set up board accordingly, and possibly other things (side to move, etc.)
def readfen(fen):
    comps = fen.split() # split into components
    setup = comps[0]
    board = Board(width, height)

    rank = height - 1 # FEN starts from last rank
    file = 0
    for c in setup:
        if c.isdigit(): # skip that many cells (already initialized to None)
            file += int(c)
        elif c == '/': # new row
            rank -= 1
            file = 0
        else: # put piece
            board.set((file,rank), c)
            file += 1

    return board

def play(board, side): # get moves from alternating sides
    N = moves.makeleaper(2,1) # knight

    while True:
        # get target piece
        s1 = drawer.getmousesquare()
        if s1.piece == None:
            continue

        # highlight
        drawer.hlsquare(s1)

        # get possible moves based on piece type
        m = N(board, s1.getloc())
        # print(moves)

        # highlight all possible moves
        for l in m:
            drawer.hlloc(l)

        # get target location, check if valid
        s2 = drawer.getmousesquare()
        if s2.getloc() in m:
            board = m[s2.getloc()]
            drawer.update(board)
        
        # undo all highlight
        drawer.unhlsquare(s1)
        for l in m:
            drawer.unhlloc(l)

def main():
    drawer.init(8,8)
    standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    board = readfen(standard)
    drawer.update(board)
    play(board, 1)


if __name__ == '__main__':
    main()
