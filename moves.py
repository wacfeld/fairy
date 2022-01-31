import copy
from objects import *
import main

'''
- [x] leapers
- [ ] riders
- [ ] not putting the king in check (royalty)
'''

'''
a proto-piece is simply a list of offsets, independent of location and surroundings of a piece

a piece is a function that takes in a board and loc and returns:
    legal locs to move to
    the resulting possible boards
(in the form of a dictionary)

to turn a proto-piece into a piece we need to:
    add the offsets to the given loc
    determine which resulting squares are legal

to do so, we have a series of modifiers, which:
    restrict possible moves
    define the results of possible moves

for example, a left-right-cylindrical modifier will allow some "illegal" coordinates by simply making them wrap around the board
a capture-by-replacement modifier simply disallows captures of friendly pieces, and allows capture of enemy pieces
a no-jumping modifier

that is to say, each modifier takes in a (loc, board) pair and either:
    returns False/None, meaning this is not allowed
    returns a new modified (loc,board) pair

therefore modifiers must be applied in order, and are not commutative
we must determine whether a move is cylindrical/noncylindrical before determine things such as capture by replacement

actually no.
cylindrical, circular modifiers, are special.

such modifiers are applied to both "dir" and "loc".
so for example, the cylindrical modifier would perform modular arithmetic on every loc after it is created
a circular modifier would be tricky, but it should be possible by modifying dir.
why is this necessary?
riders have to integrate with them
a cylindrical rider does not know where to stop. the only way is by hitting a duplicate.
if we go fully in a loop as i rider, we know to stop
then, we can filter it through ordinary modifiers such as capture by replacement
therefore to get all the rider moves, we move it as a leaper,
then we apply such special modifiers
then we add it to the candidate moves
and we loop until we hit a duplicate (the direction of the duplicate must be the same, too)
(but then how to we figure out legal moves for hoppers, etc. on a cylinder?)
right. the modifier persists. to check if something is capturing by replacement with no jumps, for example,
we simply add the direction from the src to the dest repeatedly, BUT in between each addition, we perform the aforementioned special modifiers
this way you can, for example, jump, while also moving cylindrically or circularly
therefore every "move" is this tuple:
    (src, dest, dir, board)

also to consider, some moves (such as riders?) may branch into alternatives.
therefore each modifier applied to a move should return a list of the modified moves, which is either empty (illegal move in the first place) or one, or more
'''

# all pieces come in the form of functions
# funtions are called to obtain the legal moves a piece can make on a given board at a certain location
# viz. p(board, file, rank) gets the moves for piece p
# moves are in the form of a pair of a location, and the resulting board
# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.isupper() and p2.isupper()) or (p1.islower() and p2.islower())

# makeleap simply returns  a list of location offsets that a leaper can move by
# makeleaper turns this into a piece (a function) which captures by replacement, stays within board bounds, etc.
# this facilitates the creation of riders, cylindrical pieces, etc.
def makeleap(a,b):
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
        # break down coordinates
        file = loc[0]
        rank = loc[1]

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
