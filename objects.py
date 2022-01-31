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
