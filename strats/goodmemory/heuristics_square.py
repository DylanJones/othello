from .helpers import *


def count_colors(board, color):
    """Return the number of tiles that are color - number of tiles that are opponent"""
    n = 0
    for r in board:
        for cell in r:
            if cell == color:
                n += 1
            elif cell == cinv(color):
                n -= 1
    return n


def count_legal_moves(board, color):
    """Return the number of legal moves that color has.  Supposed to be better
    than count_colors but it isn't."""
    return len(legal_moves(board, color))


# the square_weights from http://dhconnelly.com/paip-python/docs/paip/othello.html
# also happens to be the same one in othello_admin.py
SQUARE_WEIGHTS = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
]


def weight_matrix(board, color):
    """Use weight matricies to determine the heuristic value of a board."""
    s = 0
    other = cinv(color)
    for r, row in enumerate(board):
        for c, col in enumerate(row):
            if col == color:
                s += SQUARE_WEIGHTS[r][c]
            elif col == other:
                s -= SQUARE_WEIGHTS[r][c]
    return s


# -------------- Heuristic function(s) from research paper ----------------------

def mobility_score(board, color):
    # get num of moves
    lmv = count_legal_moves(board, color)
    # frontier squares
    fsq = 0


score = weight_matrix
