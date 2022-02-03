from copy import deepcopy
from objects import *
import math

# from main import height, width

# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.name.isupper() and p2.name.isupper()) or (p1.name.islower() and p2.name.islower())

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
    m = deepcopy(m)
    if not board.inbounds(m.dest): # not allowed to go out of bounds
        return []
    return [m]

# left-right cylindrical
def leftrightcyl(board, m):
    m = deepcopy(m)
    m.dest = (m.dest[0] % board.width, m.dest[1]) # wrap around on the x axis
    return nowrap(board, m) # still have to obey the top-down bounds

# nothing in the path between src and dest may be occupied, because that would be a hop
# dest can be occupied; that's a capture (presumably)
def nohop(board, m):
    # print('hey')
    # print(m.src)
    # print(m.dest)
    # print(m.aux['path'])
    m = deepcopy(m)
    for l in m.aux['path'][:-1]:
        if board.get(l) != None: # occupied
            return []
    return [m]


# basis of a rider. extends outward in given direction and adds to path in the process
# ride() is NOT an ordinary modifier! it replaces the given m with the next one in the path. it is used in extend()
def ride(board, m, pathfinder):
    # pathfinder tells how to derive the next direction(s)
    # in the case of simple riders it is just the identity function in brackets
    m = deepcopy(m)
    dir = m.dir
    newdirs = pathfinder(dir) # directions determined by pathfinder, can be 0, 1, etc.
    newmoves = [Move(m.src, addlocs(m.dest, nd), nd, m.board, m.aux, piece=m.piece) for nd in newdirs] # create new moves by adding generated directions onto current dest

    # we don't modify path yet, we wait for extend() to do that accounting for extmods
    # for nm in newmoves: # append dest to paths
    #     nm.aux['path'].append(nm.dest)
    return newmoves


def normalise(d): # normalise a direction tuple
    # currently only works on orthogonal non-zero directions!
    if d[1] != 0:
        return (d[0], d[1]/abs(d[1]))
    elif d[0] != 0:
        return (d[0]/abs(d[0]), d[1])


# restrict move by direction
# forward, backward, left, right
def direct(board, m, dirs):
    m = deepcopy(m)
    f = normalise(m.piece.forward) # normal vector telling which way is forward
    l = (-f[1], f[0]) # left
    r = (f[1], -f[0]) # right
    b = (-f[0], -f[1]) # backwards
    dirdict = {f:'f', l:'l', r:'r', b:'b'} # map tuple directions to characters (format of dirs argument)

    md = m.dir
    # split into components, normalise, convert through dictionary
    xcomp = dirdict[normalise((md[0], 0))]
    ycomp = dirdict[normalise((0, md[1]))]
    if xcomp not in dirs or ycomp not in dirs: # illegal direction
        return []
    return [m]


# no revisiting the same location in your path with the same direction
# this is important for, say, cylindrical/circular riders
def noretrace(board, m):
    m = deepcopy(m)
    path = m.aux['path']
    # note that path contains m.dest itself, so we must exclude that
    for i in range(len(path) - 1):
        dir = sublocs(path[i+1], path[i])
        if path[i] == m.dest and dir == m.dir: # both coincide, retracing found
            return []

    # if m.dest in board.aux['path']:
    #     return []

    return [m]


# def nowrap(p):
#     def q(board, src):
#         moves = p(board, src)
#         moves = list(filter(board.inbounds, moves))
#     return q

# simplest move. implies capture by replacement and leaping, regardless of enemy or friend. simply overwrites dest with src, then deletes src
def replace(board, m):
    m = deepcopy(m)

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
        newmoves = expcontr(board, moves, mod)
        return newmoves
        # newmoves = [mod(board, m) for m in moves] # list of lists of moves
        # return [m for n in newmoves for m in n] # flatten newmoves
    return q


# expand and contract. we expand l (list of moves) into a list of lits of moves via f: board, move -> listof moves
# and then flatten (contract) it
def expcontr(board, l, f):
    exp = [f(board, m) for m in l]
    newl = [m for e in exp for m in e]
    return newl


# ban friendly fire
def nofriendly(board, m):
    m = deepcopy(m)

    if 'captures' not in m.aux: # not a capture; allow
        return [m] # return unmodified

    for c in m.aux['captures']: # go through captures, remove friendly ones
        if sameside(board.get(m.src), board.get(c.loc)): # if source piece is friendly with captured location piece, ban
            if c.necessary: # totally banned
                return []
            else: # undo capture
                m.board.set(c.loc, deepcopy(board.get(c.loc)))

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


# a - b
def sublocs(a, b):
    return (a[0] - b[0], a[1] - b[1])


# make leaper generator, used by both leapers and riders
def makeleapgen(a, b):
    # sets up move destinations, accounting for possible extension by riders
    def p1(board, src):
        # get all offsets (8 total, not necessarily unique, not necessarily in bounds)
        offsets = leapoffs(a,b)

        # turn into list of Moves
        moves = [Move(src, addlocs(src, o), o, piece=board.get(src)) for o in offsets]
        return moves
    return p1


# compound a list of mods (one after another)
# ex. compmod(board, [replace, nowrap]) is a function that calls replace, then nowrap, on a move
def compmod(board, lmod):
    def res(board, m):
        moves = [m]
        for mod in lmod: # apply left to right
            moves = expcontr(board, moves, mod)
        return moves
    return res


# extend a directioned move until we cannot anymore
def extend(board, m, extmods, amt, pathfinder):
    # extmods includes both the thing to perform the extension (at the front of the list) and also any necessary filters (ex. nowrap)

    m.aux['path'] = []
    moves = []
    newmoves = [m] # calling the extension on moves every single time seems bad, so we will only operate on the newest ones
    # ^ this is guaranteed to work because we always use the same mods, so reapplying on old moves will only produce duplicates
    compext = compmod(board, extmods) # compound the extmods into one function
    i = 0
    # i increments until reaches amt
    # when amt is negative, it continues indefinitely (fullextend)
    while newmoves != [] and i != amt: # while new moves still exist
        # the ride() modifier is separated from extmods
        # because ride() replaces, and must be stored in newnewmoves
        newmoves = expcontr(board, newmoves, compext) # perform the given modifiers on the moves
        # note how this looping setup ensures that every move, including the original one passed to extend(), gets put through this
        for nm in newmoves: # add to path only after performing necessary modifications, which may include altering nm.dest, or removing altogether
            # m.src itself is not in the path! however m.dest (and everything in between) is
            nm.aux['path'].append(nm.dest)
        moves += newmoves

        i += 1
        if i == amt: # right before ending, don't need to do the rest of this iteration
            # perhaps this is a kludge, but it allows us to not specify pathfinder for leapers (amt=1)
            continue
        ridemod = lambda a, b: ride(a, b, pathfinder) # ride() itself is not a modifier, it has an extra argument
        newnewmoves = expcontr(board, newmoves, ridemod) # extend by 1

        # shift back
        newmoves = newnewmoves

    # print('hey')
    # print(m.src)
    # print([thing.dest for thing in moves])
    return moves


def makerider(a, b):
    p1 = makeleapgen(a,b) # leap generator for riders as well
    extmods = [nowrap]
    idem = lambda l: [l] # the identity location pathfinder
    extendmod = lambda a, b: extend(a, b, extmods, -1, idem)
    p2 = modify(p1, extendmod)

    p3 = modify(p2, nohop) # no hopping, the rider must only pass through unoccupied squares until the destination

    # move and capture by replacement
    p4 = modify(p3, replace)
    p5 = modify(p4, nofriendly) # no friendly fire

    return p5


# ex. makeleaper(2,1) is a knight
def makeleaper(a, b):
    p1 = makeleapgen(a,b)
    
    # p2 = modify(p1, nowrap)
    extmods = [nowrap] # no going out of bounds
    extendmod = lambda a, b: extend(a, b, extmods, 1, None)
    # do not conflate extmods with extendmod
    p2 = modify(p1, extendmod)
    # print(p2)

    # move and capture by replacement
    p3 = modify(p2, replace)
    # ban friendly fire
    p4 = modify(p3, nofriendly) # no friendly fire

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

def compound(*pieces): # e.x. Q = compound(R, B)
    def q(board, src):
        movelists = [p(board, src) for p in pieces] # get moves for each piece
        moves = [m for list in movelists for m in list] # flatten
        return moves
    return q
