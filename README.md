[fairy chess](https://en.wikipedia.org/wiki/Fairy_chess_piece)

all the standard chess piece movements can be broken down into components (e.g. a queen is a bishop plus a knight), which can then be combined with numerous modifications to create new chess pieces, call fairy chess pieces. these pieces can be incorporated into regular chess experimentally, or used in chess variants.

this project lets you play chess with any such pieces, as long as you can define them.

pieces are represented by python functions, which output legal moves for a given piece. these functions can be combined in various ways to create new pieces.

all the interesting logic is in moves.py, and the thought processes behind them are in plan.txt. a haphazard checklist listing all the currently implemented features is also there.

all the resulting pieces are in pieces.py (though you can add more). the piecemap (dictionary mapping letters to pieces) and starting FEN are in main.py, which you can experiment with.

everything is currently a work in progress; i am just experimenting with stuff myself.

dependencies:
- python3
- tkinter
