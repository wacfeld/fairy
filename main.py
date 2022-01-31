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
        s1 = drawer.getmousesquare()
        if s1.piece == None:
            continue
        drawer.hlsquare(s1)
        moves = N(board, s1.getloc())
        print(moves)

        for m in moves:
            drawer.hlsquare(m[0])
        

        s2 = drawer.getmousesquare()
        p = s1.piece
        delpiece(s1)
        placepiece(s2, p)
        unhlsquare(s1)

def main():
    drawer.init(8,8)
    standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    board = readfen(standard)
    drawer.update(board)
    input()


if __name__ == '__main__':
    main()
