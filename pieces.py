from moves import *

# basic leapers
F = makeleaper(1,1) # ferz
W = makeleaper(0,1) # wazir
A = makeleaper(2,2) # alfil
D = makeleaper(0,2) # dabbaba
N = makeleaper(2,1) # knight

B = makerider(1, 1) # bishop
R = makerider(0,1) # rook
Q = compound(B, R) # queen
K = compound(F, W) # king

NN = makerider(2,1) # nightrider

NQ = compound(Q, N) # knighted queen (amazon)
NB = compound(B, N) # knighted bishop (princess/archbishop)
NR = compound(R, N) # knighted rook (empress/chancellor)
NK = compound(K, N) # knighted king

KB = compound(B, K) # crowned bishop (dragon horse)
KR = compound(R, K) # crowned rook (dragon king)

shortR = makerider(0,1, 4) # short rook (range 4)

forW = appmod(W, direct('f')) # forward only wazir
forF = appmod(F, direct('f')) # forward only ferz

# TODO need to be able to limit range after-the-fact, for example range(R,4) is short rook
print('hey')
initP = modlist(makerider(0,1,2), [onrow(1), direct('f'), nocapt]) # initial pawn move, captures excluded
captP = modlist(F, [direct('f'), capt]) # pawns capture as forward ferzes
nocaptP = modlist(W, [direct('f'), nocapt]) # pawns move as forward wazirs



P = compound(initP, captP, nocaptP) # the pawn
# Testpiece = modlist(R, [leftrightcyl]) # cylindrical
Testpiece = R
