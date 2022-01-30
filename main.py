import drawer

'''
- [x] make a chessboard
- [x] figure out where clicks land
- [x] put pieces on the chessboard
- [x] FEN -> board
- [ ] board -> FEN
- [ ] move pieces on the chessboard
- [ ] get legal moves on chessboard, based on arbitrary fairy chess move properties
- [ ] determine check and checkmate
- [ ] make an engine that's good
- [ ] make object oriented
'''

height = 8
width = 8

# read FEN, set up board accordingly, and possibly other things (side to move, etc.)
def readfen(fen):
    comps = fen.split() # split into components
    board = comps[0]

    # clear board first
    for file in range(width):
        for rank in range(height):
            drawer.delpiece(file, rank)

    rank = height - 1 # last rank, 0-indexed
    file = 0
    for c in board:
        if c.isdigit(): # skip that many cells
            file += int(c)
        elif c == '/': # new row
            rank -= 1
            file = 0
        else: # put piece
            drawer.placepiece(file, rank, c)
            file += 1


def main():
    drawer.createboard(8,8)
    standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    readfen(standard)
    drawer.play('w')

    input()

if __name__ == '__main__':
    main()
