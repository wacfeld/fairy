from copy import deepcopy
from objects import *


# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.isupper() and p2.isupper()) or (p1.islower() and p2.islower())

# simply returns  a list of location offsets that a leaper can move by
# makeleaper turns this into a piece (a function) which captures by replacement, stays within board bounds, etc.
# this facilitates the creation of riders, cylindrical pieces, etc.
def leapoffs(a,b):
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

# no cylindrical wrapping
def nowrap(board, m):
    if not board.inbounds(m.dest): # not allowed to go out of bounds
        return []
    return [m]

# def nowrap(p):
#     def q(board, src):
#         moves = p(board, src)
#         moves = list(filter(board.inbounds, moves))
#     return q

# simplest move. implies capture by replacement and leaping, regardless of enemy or friend. simply overwrites dest with src, then deletes src
def replace(board, m):
    m.board = deepcopy(board)
    m.board.set(m.dest, m.board.get(m.src))
    m.board.set(m.src, None)
    # see if any captures occur
    if board.get(m.dest) != None: # something was captured
        m.aux['captures'] = [Capture(m.dest, True)] # add to list of things it captures
        # True indicates it is a necessary capture
    return [m]

# def replace(p):
#     def q(board, src):
#         moves = p(board, src)
#         for m in moves:
#             m.board = deepcopy(board)
#             m.board.set(m.dest, m.board.get(src))
#             m.board.set(src   , None)

#             # see if any captures occur
#             if board.get(m.dest) != None: # something was captured
#                 m.aux['captures'] = [Capture(m.dest, True)] # add to list of things it captures
#                 # True indicates it is a necessary capture

#         return moves
#     return q

# apply a modifier to a piece
def modify(p, mod):
    def q(board, src):
        moves = p(board, src)
        newmoves = [mod(board, m) for m in moves] # list of lists of moves
        return [m for n in newmoves for m in n] # flatten newmoves
    return q


# ban friendly fire
def nofriendly(board, m):
    if 'captures' not in m.aux: # not a capture; allow
        return [m] # return unmodified

    for c in m.aux['captures']: # go through captures, remove friendly ones
        if sameside(board.get(m.src), board.get(c.loc)): # if source piece is friendly with captured location piece, ban
            if c.necessary: # totally banned
                return []
            else: # undo capture
                m.board.set(c.loc, board.get(c.loc))

    # return move with all unnecessary friendly captures filtered out
    return [m]

# # either allows or disallows friendly fire
# def friendly(p, allowed):
#     if allowed == True: # then nothing needs to be changed
#         return p

    
#     def q(board, src):
#         moves = p(board, src)
#         # filter out ones where we capture our own piece
#         for m in moves:
#             if 'captures' not in m.aux: # nothing gets captured

# add two locations coordinate wise
def addlocs(a, b):
    return (a[0] + b[0], a[1] + b[1])

# make leaper generator, used by both leapers and riders
def makeleapgen(a, b):
    # sets up move destinations, accounting for possible extension by riders
    def p1(board, src):
        # get all offsets (8 total, not necessarily unique, not necessarily in bounds)
        offsets = leapoffs(a,b)

        # turn into list of Moves
        moves = [Move(src, addlocs(src, o), o) for o in offsets]
        return moves


# ex. makeleaper(2,1) is a knight
def makeleaper(a, b):
    p1 = makeleapgen(a,b)

    # get rid of out of bounds, cylindrical banned
    p2 = modify(p1, nowrap)
    # move and capture by replacement
    p3 = modify(p2, replace)
    # ban friendly fire
    p4 = modify(p3, nofriendly)

    return p4
    
    # capture by replacement, enemy pieces only

        # moves = {} # keys are locs, entries are boards
        
        # # perform moves on board
        # for l in newlocs:
        #     cboard = copy.deepcopy(board)

        #     if cboard.get(l) != None and sameside(cboard.get(l), cboard.get(loc)): # if same side, illegal move (for a leaper)
        #         continue

        #     # move piece
        #     cboard.set(l, cboard.get(loc))
        #     cboard.set(loc, None)

        #     # add to moves
        #     moves[l] = cboard

        # return moves
    return p
