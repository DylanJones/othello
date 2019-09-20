from .helpers import *
import warnings


def count_colors(board, color):
    """Return the number of tiles that are color - number of tiles that are opponent"""
    n = 0
    for cell in board:
        if cell == color:
            n += 1
        elif cell == cinv(color):
            n -= 1
    return n


def count_legal_moves(board, color):
    """Return the number of legal moves that color has.  Supposed to be better
    than count_colors but it isn't."""
    return len(legal_moves(board, color))


def weight_matrix(board, color):
    """Use weight matricies to determine the heuristic value of a board."""
    if next_player(board, color) is None:
        return count_colors(board, color) * 2 ** 24
    s = 0
    other = cinv(color)
    for i, square in enumerate(board):
        if square == color:
            s += SQUARE_WEIGHTS[i]
        elif square == other:
            s -= SQUARE_WEIGHTS[i]
    return s


def count_stable_pieces(board, color):
    tmp = [0] * 64
    num_flipped = 0
    corners = {0, 0o07, 0o70, 0o77}


# -------------- Heuristic function(s) from research paper ----------------------

def mobility_score(board, color):
    # more legal moves is better
    lmv = count_legal_moves(board, color)
    fsq_delta = frontier_squares(board, cinv(color)) - frontier_squares(board, color)
    return int(fsq_delta * 0.5) + lmv * 2


def stability_score(board, color):
    # instead of using the methods described in the paper, I will use weight matrix to simulate the stability score
    return weight_matrix(board, color)


def parity_score(board, color):
    # the paper says this is not used
    pass


def frontier_squares(board, color):
    # having fewer frontier squares than the opponent is good
    return 0
    s = 0
    for i, pos in enumerate(board):
        r, c = i // 8, i % 8
        for rstep, cstep in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r += rstep
            c += cstep
            if 0 < r < 8 and 0 < c < 8 and board[r * 8 + c] == color:
                s += 1
                break
    return s


def lineFit(a, b, c, d, x):
    if x < a:
        return b
    if x > c:
        return d
    return ((b - d) / (a - c)) * (x - a) + b


use_dynamic = False
if use_dynamic:
    ws_init = 100
    ws_final = 2
    ws_start_t = 25
    ws_end_t = 64
else:
    ws_init = 10
    ws_final = 10
    ws_start_t = 5
    ws_end_t = 64
WEIGHT_STAGE_SQ = [lineFit(ws_start_t, ws_init, ws_end_t, ws_final, x) for x in range(65)]
if use_dynamic:
    lm_start_t = 5
    lm_init = 1
    lm_end_t = 58
    lm_final = 30
else:
    lm_start_t = 5
    lm_init = 1
    lm_end_t = 64
    lm_final = 1
WEIGHT_STAGE_MOVE = [lineFit(lm_start_t, lm_init, lm_end_t, lm_final, x) for x in range(65)]
# during the last few turns, moves are INCREDIBLY important
if use_dynamic:
    for i in range(59, 65):
        WEIGHT_STAGE_MOVE[i] = lineFit(lm_end_t, lm_final, 64, 50, i)


def research_paper_heuristic(board, color):
    # msc = mobility_score(board, color)
    # ssc = stability_score(board, color)
    # return ssc * 100 + msc
    if next_player(board, color) is None:
        return count_colors(board, color) * 10 ** 10
    # return count_legal_moves(board, color) + frontier_squares(board, color) + weight_matrix(board, color) * 10
    stage = 64 - board.count(EMPTY)
    return count_legal_moves(board, color) * WEIGHT_STAGE_MOVE[stage] + \
           weight_matrix(board, color) * WEIGHT_STAGE_SQ[stage] + \
           frontier_squares(board, color)


# score = weight_matrix
score = research_paper_heuristic
try:
    from .machine_code import frontier_squares
    from .machine_code import count_colors
    from .machine_code import weight_matrix
except RuntimeError:
    warnings.warn("Failed to import machine code - falling back to slow python-only implementation", RuntimeWarning)
