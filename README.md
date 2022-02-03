fairy chess

all the standard chess piece movements can be broken down into components (e.g. a queen is a bishop plus a knight), which can then be combined with various modifications to create new chess pieces, call fairy chess pieces. these pieces can be incorporated into regular chess experimentally, or used in chess variants.

this project lets you play chess with any such pieces, as long as you can define them.

pieces are represented by python functions, which output legal moves for a given piece. these functions can be combined in various ways to create new pieces.

all the interesting logic is in moves.py, and the thought processes behind them are in plan.txt

dependencies:
- python3
- tkinter
