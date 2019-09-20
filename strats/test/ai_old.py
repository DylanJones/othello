#!/usr/bin/env python3
"""
This module contains the various decision making functions.
"""
from .helpers import *
from .heuristics import score
from random import choice, shuffle
import time

NEGATIVE_INF = -(2 ** 80)
POSITIVE_INF = 2 ** 80


def random(board, color):
    """Make a random move."""
    moves = legal_moves(board, color)
    return choice(moves)


def human(board, color):
    """Prompt the user for a move."""
    moves = legal_moves(board, color)
    move = None
    while True:
        s = input("Enter the coordinates for a move >>> ")
        try:
            move = tuple(int(x.strip()) for x in s.split(','))
            if move in moves:
                break
            else:
                raise RuntimeError()
        except:
            print("Please enter a valid move.")
    return move


def lookahead_n(board, color, n):
    mv = None
    best = NEGATIVE_INF
    # so stupid.  apparently we want to minimize our score instead of maximize it?
    # best = 3842489432
    for move in legal_moves(board, color):
        board2 = [b[:] for b in board]
        # board2[move[0]][move[1]] = color
        make_move(board2, color, move)
        num = lookahead_helper(board2, color, n, next_player(board2, color))
        if num > best:
            best = num
            mv = move
    return mv


def lookahead_helper(board, color, depth, nextmv):
    if depth == 0:
        return score(board, color)
    best = NEGATIVE_INF
    # seriously - this makes no sense.
    # best = 342894366
    for move in legal_moves(board, nextmv):
        board2 = [b[:] for b in board]
        # board2[move[0]][move[1]] = color
        make_move(board, nextmv, move)
        num = lookahead_helper(board2, color, depth - 1, next_player(board2, nextmv))
        if num > best:
            best = num
    return best


def minimax(board, color, n):
    best_min = NEGATIVE_INF
    best_move = None
    for move in legal_moves(board, color):
        board2 = copy_board(board)
        make_move(board2, color, move)
        mmx = minimax_helper(board2, color, color, n)
        if mmx > best_min:
            best_move = move
            best_min = mmx
    return best_move


def minimax_helper(board, color, last_color, depth):
    moving_plr = next_player(board, last_color)
    if moving_plr == None or depth == 0:
        return score(board, color)
    best = NEGATIVE_INF if moving_plr == color else POSITIVE_INF
    for move in legal_moves(board, moving_plr):
        board2 = copy_board(board)
        make_move(board2, moving_plr, move)
        worstcase = minimax_helper(board2, color, moving_plr, depth - 1)
        if moving_plr == color:  # pick the move with the best worse-case
            if worstcase > best:
                best = worstcase
        else:  # other player's turn - pick the worst case
            if worstcase < best:
                best = worstcase
    return best


def minimax_helper2(board, color, last_color, depth):
    moving_plr = next_player(board, last_color)
    if moving_plr == None or depth == 0:
        return score(board, color)
    if moving_plr == cinv(color):
        return minimax_helper2(board, cinv(color), last_color, depth)
    best = NEGATIVE_INF
    for move in legal_moves(board, moving_plr):
        # board2 = [list(b) for b in board]
        board2 = copy_board(board)
        make_move(board2, moving_plr, move)
        worstcase = minimax_helper2(board2, color, moving_plr, depth - 1)
        if worstcase > best:
            best = worstcase
    return best


# node format (UNUSED, SHOULD DELETE COMMENT):
# 0 - board
# 1 - board array pointer
# 2 - who moved to get this state
# 3 - legal_moves for us
# 4 - legal_moves for them
# 5 - zorbist hash
# 6 - heuristic score
# 7 - depth that we searched down from this node


def alphabeta(board, color, n):
    best_min = NEGATIVE_INF
    best_move = None
    for move in legal_moves(board, color):
        board2 = copy_board(board)
        make_move(board2, color, move)
        #mmx = alphabeta_helper_memory(board2, color, NEGATIVE_INF, POSITIVE_INF, color, n)
        mmx = alphabeta_helper(board2, color, NEGATIVE_INF, POSITIVE_INF, color, n)
        if mmx > best_min:
            best_move = move
            best_min = mmx
    # print(f'Overall best: {best_move} with score {best_min}')
    return best_move

def alphabeta_helper(board, color, alpha, beta, last_color, depth):
    moving_plr = next_player(board, last_color)
    if moving_plr is None or depth == 0:
        return score(board, color)
    best = NEGATIVE_INF if moving_plr == color else POSITIVE_INF
    moves = legal_moves(board, moving_plr)
    for move in moves:
        board2 = copy_board(board)
        make_move(board2, moving_plr, move)
        mmx = alphabeta_helper(board2, color, alpha, beta, moving_plr, depth - 1)
        if moving_plr == color:
            best = max(best, mmx)
            alpha = max(best, alpha)
        else:
            best = min(best, mmx)
            beta = min(best, beta)
        if beta <= alpha:  # alpha-beta cutoff
            break
    return best

def alphabeta_helper_memory(board, color, alpha, beta, last_color, depth):
    moving_plr = next_player(board, last_color)
    if moving_plr is None or depth == 0:
        return score(board, color)
    best = NEGATIVE_INF if moving_plr == color else POSITIVE_INF
    moves = legal_moves(board, moving_plr)
    nmv = []
    for move in moves:
        cval = transposition_lookup(board, moving_plr)
        if cval is not None:
            nmv.append((cval[0], cval[1], move))
        else:
            nmv.append((-1, -1, move))
    nmv.sort(key=lambda x: x[1], reverse=False)
    for node in nmv:
        if node[0] < depth:
            # print("mss", node[0], node[1])
            board2 = copy_board(board)
            make_move(board2, moving_plr, node[2])
            mmx = alphabeta_helper_memory(board2, color, alpha, beta, moving_plr, depth - 1)
        else:
            print("hit", node[0], node[1])
            mmx = node[1]
        if moving_plr == color:
            best = max(best, mmx)
            alpha = max(best, alpha)
        else:
            best = min(best, mmx)
            beta = min(best, beta)
        if node[0] < depth:
            # add this to transpose
            transposition_add(board, moving_plr, depth-1, mmx)
        if beta <= alpha:  # alpha-beta cutoff
            break
    return best


def get_move(board, player, best_move, still_running):
    """Get the best move for specified player"""
    i = 1
    while still_running.value and i < 20:  # too much
        s = time.time()
        mv = alphabeta(board, player, i)
        print(len(cache))
        print(f"alphabeta: {time.time()-s} seconds for i={i}")
        pStat()
        jmv = to_tournament_move(mv)
        best_move.value = jmv
        i += 1
    return mv
