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
            f = (0,1) if c.isupper() else (0,-1)
            board.set((file,rank), Piece(c, forward=f))
            file += 1

    return board

piecemap = {
        'k': pieces.K,
        'q': pieces.Q,
        'r': pieces.R,
        'b': pieces.B,
        'n': pieces.N,
        'K': pieces.K,
        'Q': pieces.Q,
        'R': pieces.R,
        'B': pieces.B,
        'N': pieces.N,
        'p': pieces.P,
        'P': pieces.P,
        }


def play(board, side): # get moves from alternating sides
    # TODO implement one-square multiple moves thing. will matter for cylindrical moves etc.
    drawer.update(board)
    while True:
        # get target piece
        l1 = drawer.getmousesquare().getloc()
        if board.get(l1) == None:
            continue

        # highlight
        drawer.hlloc(l1)

        # get possible moves based on piece type
        # piece = piecemap[board.get(l1).name]
        piece = pieces.Testpiece
        moves = piece(board, l1)
        # print(moves)

        movedests = [m.dest for m in moves]
        # highlight all possible destinations
        for d in movedests:
            drawer.hlloc(d)

        # destdict = {m.dest:m.board for m in moves} # dictionary mapping destinations to boards

        # get target location, check if valid
        l2 = drawer.getmousesquare().getloc()
        if l2 in movedests: # legal move
            boards = [m.board for m in moves if m.dest == l2] # get all resulting boards with that destination
            # moves = [m for m in moves if m.dest == l2]
            # print(moves[0].aux['path'])
            # TODO implement check to see if all boards are same, in which case go ahead
            # otherwise need some way to select which move to make, perhaps by highlighting path and all side effects
            # (by simple before-after comparison)

            # at the moment, pick the first one
            board = boards[0]

            # board = destdict[l2]

            drawer.update(board)
        
        # undo all highlight
        drawer.unhlloc(l1)
        for l in movedests:
            drawer.unhlloc(l)

def main():
    drawer.init(width, height)
    standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    testfen = '88/88/88/88/88/88/88/88/88/88/88/88/88/88/88/8NNNNnnnn w KQkq - 0 1'
    checkers = '1p1p1p1p/p1p1p1p1/1p1p1p1p/8/8/P1P1P1P1/1P1P1P1P/P1P1P1P1 w KQkq - 0 1'

    board = readfen(checkers)
    play(board, 1)


if __name__ == '__main__':
    main()
