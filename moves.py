from copy import deepcopy
from objects import *
from inspect import signature
import pathfinders
import math

# from main import height, width

# i wanted to do this in lisp but i couldn't figure out how to integrate that with python, so here we are

def diradj(d):
    dirs = leapoffs(*d) # get ordered distinct directions
    numdirs = len(dirs)
    idx = dirs.index(d)
    adj1 = dirs[(idx + 1) % numdirs]
    adj2 = dirs[(idx - 1) % numdirs]
    return [adj1, adj2]


# flatten([[1, 2], [3, 4]]) = [1, 2, 3, 4]
def flatten(ll):
    return [x for l in ll for x in l]


# check if two pieces are on the same side
def sameside(p1, p2):
    return (p1.name.isupper() and p2.name.isupper()) or (p1.name.islower() and p2.name.islower())

# simply returns  a list of location offsets that a leaper can move by
# makeleaper turns this into a piece (a function) which captures by replacement, stays within board bounds, etc.
# this facilitates the creation of riders, cylindrical pieces, etc.
def leapoffs(a,b):
    # the order listed is important, as it will be used to create circular/crooked riders
    # the order is where all adjacent directions are adjacent in the list (it's a circle)

    # without the absolute values then diradj((-1,1)) is broken. have not looked into it
    a = abs(a)
    b = abs(b)
    a, b = max(a, b), min(a, b) # required to make the circles not ovals
    offsets = [
            (+a, +b),
            (+b, +a),
            (-b, +a),
            (-a, +b),
            (-a, -b),
            (-b, -a),
            (+b, -a),
            (+a, -b),
            ]
    # remove duplicates (e.x. a (2,2) leaper has only 4 moves, not 8
    # offsets = list(set(offsets))
    offsets = list(dict.fromkeys(offsets))
    # it seems that dict.fromkeys() preserves order while set() does not

    return offsets

# no cylindrical wrapping
def nowrap(board, m):
    # m = deepcopy(m)
    if not board.inbounds(m.dest): # not allowed to go out of bounds
        return []
    return [m]

# left-right cylindrical
def leftrightcyl(board, m):
    # m = deepcopy(m)
    m.dest = (m.dest[0] % board.width, m.dest[1]) # wrap around on the x axis
    return [m]
    # return nowrap(board, m) # still have to obey the top-down bounds

# not very useful for standard chess, but here for completeness
def updowncyl(board, m):
    # m = deepcopy(m)
    m.dest = (m.dest[0], m.dest[1] % board.height) # wrap around on the y axis
    return [m]
    # return nowrap(board, m) # still have to obey the left-right bounds


# in same quadrant of cartesian plane (being on boundaries allowed too)
def samequad(d1, d2):
    return (d1[0] * d2[0] >= 0) and (d1[1] * d2[1] >= 0)


# the move's direction of destination must be outward from the previous src
# useful for bent riders, etc.
# special type of modifier that can only be applied to a subsequent move (in chaining)
# prev is a tuple (prevboard, prevm)
def outward(board, m, prev):
    # m = deepcopy(m)
    prevm = prev[1]
    refdir = sublocs(m.src, prevm.src) # reference direction
    curdir = m.dir
    if samequad(refdir, curdir):
        return [m]
    return []


# take in lambda, filter moves by path len
def prunelen(f):
    def q(board, m):
        # m = deepcopy(m)
        pathlen = len(m.aux['path']) # path len determined by number of leaps
        if f(pathlen):
            return [m]
        else:
            return []
    return q


# nothing in the path between src and dest may be occupied, because that would be a hop
# dest can be occupied; that's a capture (presumably)
def nohop(board, m):
    # print('hey')
    # print(m.src)
    # print(m.dest)
    # print(m.aux['path'])
    # m = deepcopy(m)
    for l in m.aux['path'][:-1]:
        if board.get(l) != None: # occupied
            return []
    return [m]


# wrapper
def onrow(r, src=True):
    return lambda a,b: onrowmod(a, b, r, src)

# check which row the piece starts/ends on, from that player's perspective
# useful for pawns (initial move, promotion)
# "row" here is relative to the forward direction, so it can either be ranks or files
def onrowmod(board, m, r, src=True):
    # m = deepcopy(m)
    forward = normalise(m.piece.forward) # assuming this is orthogonal
    rankorfile = 1 if forward[1] != 0 else 0 # whether to go by rank or file

    boardlen = board.height if rankorfile == 1 else board.width

    loc = m.src if src else m.dest # whether to look at start or endpoint
    row = loc[rankorfile]

    if forward[rankorfile] < 0: # reversed, start from high end of board
        row = boardlen - row - 1
    if r == row: # matches requirement
        return [m]
    return []


# basis of a rider. extends outward in given direction and adds to path in the process
# ride() is NOT an ordinary modifier! it replaces the given m with the next one in the path. it is used in extend()
def ride(board, m, pf):
    # pf tells how to derive the next direction(s)
    # in the case of simple riders it is just the identity function in brackets
    # m = deepcopy(m)
    dir = m.dir
    newdirs = pf(m) # directions determined by pf, can be 0 or more
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


# wrapper
def direct(d):
    return lambda a,b: dirmod(a, b, d)

# TODO replace normalise by dividing by gcd
# restrict move by direction
# forward, backward, left, right
def dirmod(board, m, dirs):
    # m = deepcopy(m)
    f = normalise(m.piece.forward) # normal vector telling which way is forward
    l = (-f[1], f[0]) # left
    r = (f[1], -f[0]) # right
    b = (-f[0], -f[1]) # backwards
    dirdict = {f:'f', l:'l', r:'r', b:'b'} # map tuple directions to characters (format of dirs argument)

    md = m.dir
    # split into components, normalise, convert through dictionary
    xcomp = dirdict.get(normalise((md[0], 0)), '-')
    ycomp = dirdict.get(normalise((0, md[1])), '-')
    # ^^^ default value '-', which is not a direction
    if xcomp not in dirs and ycomp not in dirs: # illegal direction
        # move up and right diagonally counts as moving up
        # therefore only one component has to satisfy the requirements
        return []
    return [m]


# no revisiting the same location in your path with the same direction
# this is important for, say, cylindrical/circular riders
def noretrace(board, m):
    # m = deepcopy(m)
    path = m.aux['path']
    fullpath = [m.src] + path
    # note that path contains m.dest itself, so we must exclude that
    for i in range(1,len(fullpath) - 1):
        dir = sublocs(fullpath[i], fullpath[i-1]) # where you are coming from is your dest, not where you are going
        if fullpath[i] == m.dest and dir == m.dir: # both coincide, retracing found
        # if fullpath[i] == m.dest:
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
    # m = deepcopy(m)

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


# invert a filter modifier (one that either returns [m] or [])
# this cannot always be applied, ex. applying this to nowrap would preserve out-of-bounds destinations
def invmod(mod):
    def q(board, m):
        # m = deepcopy(m)
        moves = mod(board, m)
        if moves == []:
            return [m]
        else:
            return []
    return q


# only allowed if capture takes place
def capt(board, m):
    if 'captures' in m.aux: # capture takes place
        return [m]
    return []
    
# opposite
nocapt = invmod(capt)


# apply modifiers in a list, left to right
def modlist(p, ml):
    for m in ml:
        p = modify(p, m)
    return p

# apply a modifier to a piece
def modify(p, mod):
    def q(board, src, prev=None):
        # prev is used for chaining

        moves = p(board, src)

        newmod = mod # in case no chaining, change nothing
        if prev != None: # we are chaining
            # check if mod supports chaining
            params = signature(mod).parameters
            if 'prev' in params: # does support, pass on
                newmod = lambda a, b: mod(a, b, prev)
            # otherwise, treat as regular mod, don't pass on

        newmoves = expcontr(board, moves, newmod)
        return newmoves
        # newmoves = [modify(board, m) for m in moves] # list of lists of moves
        # return [m for n in newmoves for m in n] # flatten newmoves
    return q


# expand and contract. we expand l (list of moves) into a list of lits of moves via f: board, move -> listof moves
# and then flatten (contract) it
def expcontr(board, l, f):
    exp = [f(board, deepcopy(m)) for m in l]
    # newl = [m for e in exp for m in e]
    newl = flatten(exp)
    return newl


# ban friendly fire
def nofriendly(board, m):
    # m = deepcopy(m)

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
    # print(a, b)
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


# wrapper
def extend(extmods, amt, pf):
    return lambda a, b: extendmod(a, b, extmods, amt, pf)

# extend a directioned move until we cannot anymore
def extendmod(board, m, extmods, amt, pf):
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
            # perhaps this is a kludge, but it allows us to not specify pf for leapers (amt=1)
            continue
        ridemod = lambda a, b: ride(a, b, pf) # ride() itself is not a modifier, it has an extra argument
        newnewmoves = expcontr(board, newmoves, ridemod) # extend by 1

        # shift back
        newmoves = newnewmoves

    # print('hey')
    # print(m.src)
    # print([thing.dest for thing in moves])
    return moves

# boundkeepers = [updowncyl, leftrightcyl, noretrace]
# boundkeepers = [noretrace, nowrap]
boundkeepers = [nowrap]

def makerider(
        leap,
        range=-1,
        pf=pathfinders.idem,
        extmods=[nowrap, noretrace],
        aftmods=[nohop, replace, nofriendly]
        ):
    p1 = makeleapgen(*leap) # leap generator for riders as well
    # extmods = boundkeepers
    # idem = lambda l: [l] # the identity location pathfinder
    # # extendmod = lambda a, b: extend(a, b, extmods, range, idem)
    # p2 = modify(p1, extend(extmods, range, idem))

    # p3 = modify(p2, nohop) # no hopping, the rider must only pass through unoccupied squares until the destination

    # # move and capture by replacement
    # p4 = modify(p3, replace)
    # p5 = modify(p4, nofriendly) # no friendly fire

    # extmods = boundkeepers
    # p5 = modlist(p1, [
    #     extend(extmods, range, pf),
    #     nohop,
    #     replace,
    #     nofriendly
    #     ])
    p5 = modlist(p1,
            [extend(extmods, range, pf)]
            + aftmods
            )

    return p5


# ex. makeleaper(2,1) is a knight
def makeleaper(a, b):
    p1 = makeleapgen(a,b)
    
    # # p2 = modify(p1, nowrap)
    # extmods = boundkeepers # no going out of bounds
    # # extendmod = lambda a, b: extend(a, b, extmods, 1, None)
    # # do not conflate extmods with extendmod
    # p2 = modify(p1, extend(extmods, 1, None))
    # # print(p2)

    # # move and capture by replacement
    # p3 = modify(p2, replace)
    # # ban friendly fire
    # p4 = modify(p3, nofriendly) # no friendly fire

    # idem = lambda l: [l] # the identity location pathfinder
    extmods = boundkeepers
    p4 = modlist(p1, [
        extend(extmods, 1, None),
        replace,
        nofriendly
        ])

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

def add(*pieces): # e.x. Q = add(R, B)
    def q(board, src):
        movelists = [p(board, src) for p in pieces] # get moves for each piece
        # moves = [m for list in movelists for m in list] # flatten
        moves = flatten(movelists)
        return moves
    return q


# how to merge each type of aux entry
# this is not ideal, ideally there would be no disconnect between the actual setting of auxes and how to merge them
# however we need moves to occur independent of each other until they merge at the end
auxmerges = {
        'path': lambda a, b: a + b,    # concatenate
        'captures': lambda a, b: a + b # concatenate
        }


# if a piece makes two moves in a row, then their src, aux, etc. need to be merged
def mergemoves(m1, m2):
    m1 = deepcopy(m1)
    m2 = deepcopy(m2)
    m = m2 # inherits proper dest, dir, board, part of aux
    m.src = m1.src # set proper src (the first one)
    for a in m1.aux: # merge aux
        if a not in m2.aux: # not in m2, no need to merge
            m.aux[a] = m1.aux[a]
        else:
            merge = auxmerges[a] # get merge function for this type of aux
            m.aux[a] = merge(m.aux[a], m1.aux[a]) # merge each of them

    # not sure what to do if piece changes, but for now we will just make it the same as m2, the final piece

    return m


# chain piece moves together, one after another
def chain(*pieces):
    def q(board, src):
        # cursitus = [(src, board)] # current situations, consisting of board and src
        curmoves = pieces[0](board, src) # get first set of moves to work off of
        for p in pieces[1:]: # iterate through the rest and continue the process
            newp = p
            params = signature(p).parameters

            # newmoves = [(m, p(m.board, m.dest)) for m in curmoves] # old dest becomes new src
            newmoves = []
            for m in curmoves:
                if 'prev' in params: # it's a chained piece, which requires info about the previous move
                    newp = lambda a, b: p(a, b, (None,m))
                    # TODO right now moves only contain the board after the move is made
                    # cleary this is not sufficient as seen in the tuple above. we need the board before and after
                    # until that is implemented, only the move can be passed on through prev, not the board, when chaining
                newmoves.append((m, newp(m.board, m.dest)))
            # newmoves is a list of tuples containing parent move and list of child moves

            merged = [[mergemoves(tup[0], child) for child in tup[1]] for tup in newmoves]
            # curmoves = [m for x in merged for m in x] # flatten
            curmoves = flatten(merged)

        return curmoves

    return q

print(diradj((1,2)))
