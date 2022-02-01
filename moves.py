import copy
from objects import *
import main


# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.isupper() and p2.isupper()) or (p1.islower() and p2.islower())

# simply returns  a list of location offsets that a leaper can move by
# makeleaper turns this into a piece (a function) which captures by replacement, stays within board bounds, etc.
# this facilitates the creation of riders, cylindrical pieces, etc.
def protoleap(a,b):
    offsets = [
            (-a, -b),
            (-a, +b),
            (+a, -b),
            (+a, +b),
            (-b, -a),
            (-b, +a),
            (+b, -a),
            (+b, +a),
            ]
    # remove duplicates (e.x. a (2,2) leaper has only 4 moves, not 8
    offsets = list(set(offsets))

    return offsets

# ex. makeleaper(2,1) is a knight
def makeleaper(a, b):
    def p(board, loc):
        # get all candidate moves (8 total, not necessarily unique)
        offsets = makeleap(a,b)
        newlocs = [addlocs(loc, x) for x in offsets] # add offsets to loc

        # filter out illegal coordinates
        newlocs = list(filter(lambda x: board.inbounds(x), newlocs))

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
