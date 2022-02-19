from moves import *
import pathfinders

# basic leapers
F = makeleaper(1,1) # ferz
W = makeleaper(0,1) # wazir
A = makeleaper(2,2) # alfil
D = makeleaper(0,2) # dabbaba
N = makeleaper(2,1) # knight

B = makerider((1, 1)) # bishop
R = makerider((0,1)) # rook
Q = add(B, R) # queen
K = add(F, W) # king

NN = makerider((2,1)) # nightrider

NQ = add(Q, N) # knighted queen (amazon)
NB = add(B, N) # knighted bishop (princess/archbishop)
NR = add(R, N) # knighted rook (empress/chancellor)
NK = add(K, N) # knighted king

KB = add(B, K) # crowned bishop (dragon horse)
KR = add(R, K) # crowned rook (dragon king)

# shortR = makerider((0,1), 4) # short rook (range 4)
shortR = makerider((0,1), aftmods=[nohop, replace, nofriendly, prunelen(lambda x: x <= 4)])
# slipR = makerider((0,1), aftmods=[nohop, replace, nofriendly, prunelen(lambda x: x % 2 == 1)])
# skipR = makerider((0,1), aftmods=[nohop, replace, nofriendly, prunelen(lambda x: x % 2 == 0)])
# skipR = makerider((0,2))
# unshortR = makerider((0,1), aftmods=[nohop, replace, nofriendly, prunelen(lambda x: x >= 4)])

# TODO implement these as three functions (ski, skip, slip)
# will likely require the representation of pieces as objects containing extmods, aftmods, range, amt, etc.
skiR = chain(modify(W,nocapt), modify(R, diraway))
skipR = makerider((0,2))
slipR = add(W, chain(modify(W, nocapt), modify(makerider((0,2)), diraway)))

forW = modify(W, direct('f')) # forward only wazir
forF = modify(F, direct('f')) # forward only ferz

# TODO need to be able to limit range after-the-fact, for example range(R,4) is short rook
initP = modlist(makerider((0,1),2), [onrow(1), direct('f'), nocapt]) # initial pawn move, captures excluded
captP = modlist(F, [direct('f'), capt]) # pawns capture as forward ferzes
nocaptP = modlist(W, [direct('f'), nocapt]) # pawns move as forward wazirs

P = add(initP, captP, nocaptP) # the pawn

# moves once like a Ferz (F), then optionally like a Rook, outward from original location (modify(R, outward))
FtR = add(F, chain(modify(F, nocapt), modify(R, outward))) # ferz then rook (aanca/gryphon)
# TODO make a modifier that bans intermediate captures so that we don't have to manually put nocapt on the second ferz
# or, simply something that uses chain but modifies with outward, nocapt, add, as needed to get the desired result
NtB = add(N, chain(modify(N, nocapt), modify(B, outward))) # knight then bishop (unicorn)
WtB = add(W, chain(modify(W, nocapt), modify(B, outward))) # wazir then bishop

Rose = makerider((1,2), pf=pathfinders.circular) # circular knight
Boyscout = makerider((1,1), pf=pathfinders.crooked) # crooked bishop

hopR = makerider((0,1), aftmods=[hop, replace, nofriendly])
Cannon = add(modify(R, nocapt), modify(hopR, capt)) # chinese chess cannon. no capture like rook, capture like hopping rook

locR = modlist(hopR, [nocapt, locust, nofriendly])
shootRook = makerider((0,1), aftmods=[nohop, replace, nofriendly, shoot])


Checker = add(modlist(F, [nocapt, direct('f')]), makerider((1,1), aftmods=[replace, nocapt, hop, locust, nofriendly, prunelen(lambda x: x == 2), direct('f')]))
Testpiece = Checker

# Testpiece = modlist(R, [leftrightcyl]) # cylindrical
# Testpiece = modify(F, direct('fr'))
# Testpiece = add(makerider((3,1)), NN, makerider((3,2)), Q, makerider((3,4)), makerider((3,5)), makerider((8,1)))
