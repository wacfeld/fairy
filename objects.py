class Square:
    def __init__(self):
        self.rank = None
        self.file = None
        self.color = None # color_rgb
        self.rect = None # Rectangle
        self.hl = None # Rectangle
        self.piece = None # character
        self.pieceimg = None # Image
    
    def getloc(self):
        return (self.file, self.rank)

class Piece:
    def __init__(self, name, forward=None):
        self.name = name
        self.forward = forward # which direction is considered forward, in the form of a tuple
        # at the moment only (n, 0) and (0, n) tuples are supported

class Board:
    def __init__(self, width=None, height=None): # init with board created for us
        # i guess this is how you overload methods in python

        self.width = width
        self.height = height

        if width != None and height != None:
            self.board = [[None for h in range(height)] for w in range(width)]

    # get square given coordinates
    def get(self, loc):
        file = loc[0]
        rank = loc[1]
        return self.board[file][rank]

    # set square given coordinates and piece
    def set(self, loc, piece):
        file = loc[0]
        rank = loc[1]
        self.board[file][rank] = piece

    # check if coordinates are in bounds of board
    def inbounds(self, loc):
        file = loc[0]
        rank = loc[1]
        return (0 <= file < self.width) and (0 <= rank < self.height)

class Capture:
    def __init__(self, loc=None, necessary=None):
        self.loc = loc
        self.necessary = necessary

class Move:
    # def __init__(self, src=None, dest=None, dir=None, board=None, aux={}):
    # ^^^ this breaks because the dictionary gets shared, like a pointer, bafflingly
    def __init__(self, src=None, dest=None, dir=None, board=None, aux=None, piece=None):
        self.src   = src   # where we start
        self.dest  = dest  # where we end up
        self.dir   = dir   # how we get there
        self.board = board # result & side effects
        if aux != None:
            self.aux = aux # any other information about how we move (a dictionary)
        else:
            self.aux = {}
        self.piece = piece
