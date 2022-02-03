import drawer
import moves
import pieces
from objects import *


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
    drawer.update(board)
    N = pieces.W
    while True:
        # get target piece
        l1 = drawer.getmousesquare().getloc()
        if board.get(l1) == None:
            continue

        # highlight
        drawer.hlloc(l1)

        # get possible moves based on piece type
        moves = N(board, l1)
        print(moves)

        # highlight all possible destinations
        for m in moves:
            drawer.hlloc(m.dest)

        destdict = {m.dest:m.board for m in moves} # dictionary mapping destinations to boards

        # get target location, check if valid
        l2 = drawer.getmousesquare().getloc()
        if l2 in destdict: # legal move
            board = destdict[l2]
            drawer.update(board)
        
        # undo all highlight
        drawer.unhlloc(l1)
        for l in destdict:
            drawer.unhlloc(l)

def main():
    drawer.init(8,8)
    standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    board = readfen(standard)
    play(board, 1)


if __name__ == '__main__':
    main()
