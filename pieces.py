from moves import *

# basic leapers
F = makeleaper(1,1) # ferz
W = makeleaper(0,1) # wazir
A = makeleaper(2,2) # alfil
D = makeleaper(0,2) # dabbaba
N = makeleaper(2,1) # knight

B = makerider(1, 1) # bishop
R = makerider(0,1) # rook
Q = add(B, R) # queen
K = add(F, W) # king

NN = makerider(2,1) # nightrider

NQ = add(Q, N) # knighted queen (amazon)
NB = add(B, N) # knighted bishop (princess/archbishop)
NR = add(R, N) # knighted rook (empress/chancellor)
NK = add(K, N) # knighted king

KB = add(B, K) # crowned bishop (dragon horse)
KR = add(R, K) # crowned rook (dragon king)

shortR = makerider(0,1, 4) # short rook (range 4)

forW = modify(W, direct('f')) # forward only wazir
forF = modify(F, direct('f')) # forward only ferz

# TODO need to be able to limit range after-the-fact, for example range(R,4) is short rook
initP = modlist(makerider(0,1,2), [onrow(1), direct('f'), nocapt]) # initial pawn move, captures excluded
captP = modlist(F, [direct('f'), capt]) # pawns capture as forward ferzes
nocaptP = modlist(W, [direct('f'), nocapt]) # pawns move as forward wazirs

P = add(initP, captP, nocaptP) # the pawn

FtR = chain(F, modify(R, outward)

# Testpiece = modlist(R, [leftrightcyl]) # cylindrical
# Testpiece = modify(F, direct('fr'))
# Testpiece = add(makerider(3,1), NN, makerider(3,2), Q, makerider(3,4), makerider(3,5), makerider(8,1))
