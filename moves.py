import copy
from objects import *

'''
- [x] leapers
- [ ] riders
- [ ] not putting the king in check (royalty)
'''

# all pieces come in the form of functions
# funtions are called to obtain the legal moves a piece can make on a given board at a certain location
# viz. p(board, file, rank) gets the moves for piece p
# moves are in the form of a pair of a location, and the resulting board
# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.isupper() and p2.isupper()) or (p1.islower() and p2.islower())

# ex. makeleaper(2,1) is a knight
def makeleaper(a, b):
    def p(board, loc):
        # break down coordinates
        file = loc[0]
        rank = loc[1]

        # get all candidate moves (8 total, not necessarily unique)
        newlocs = [
                (file - a, rank - b),
                (file - a, rank + b),
                (file + a, rank - b),
                (file + a, rank + b),
                (file - b, rank - a),
                (file - b, rank + a),
                (file + b, rank - a),
                (file + b, rank + a),
                ]

        # filter out illegal coordinates
        newlocs = list(filter(lambda x: board.inbounds(x), newlocs))
        # remove duplicates (e.x. a (2,2) leaper has only 4 moves, not 8
        newlocs = list(set(newlocs))

        moves = {} # keys are locs, entries are boards
        
        # perform moves on board
        for l in newlocs:
            cboard = copy.deepcopy(board)

            if cboard.get(l) != None and sameside(cboard.get(l), cboard.get(loc)): # if same side, illegal move (for a leaper)
                continue

            # move piece
            cboard.set(l, cboard.get(loc))
            cboard.set(loc, None)

            # add to moves
            moves[l] = cboard

        return moves
    return p
