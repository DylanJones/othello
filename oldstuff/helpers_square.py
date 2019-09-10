#!/usr/bin/env python3
from functools import lru_cache


def copy_board(board):
    return [list(b) for b in board]


def to_tournament_move(move):
    return (move[0] + 1) * 10 + move[1] + 1


def cacher_tupleize(func):
    """Like LRU cache but always convert first arg to tuple"""
    cfunc = lru_cache(2 ** 24, True)(func)

    def f(lst, *args, **kwargs):
        tpl = tuple(tuple(x) for x in lst)
        # print(args, kwargs)
        return cfunc(tpl, *args, **kwargs)

    return f


bsize = 8


def print_board(board):
    for r in board:
        print("\x1b[4m", end='')
        for c in r:
            print(c, end='|')
        print('\x1b[0m')
    print()


def cinv(c):
    """Color invert - change the color to the other color"""
    return 'o' if c == '@' else '@'


@cacher_tupleize
def legal_moves(board, color):
    moves = []
    for r, row in enumerate(board):
        for c, spot in enumerate(row):
            if spot == '.':  # it might be a legal move
                # check all directions
                for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if check_direction(board, color, r, c, *direction):
                        moves.append((r, c))
                        break
    return moves


@cacher_tupleize
def get_bracket_indices(board, r, c, other_color):
    all_brackets = set()
    for rstep, cstep in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        # print(rstep, cstep)
        cr, cc = r, c
        tiles = {(cr, cc)}
        cr += rstep
        cc += cstep
        iterated = False
        while 0 <= cr < bsize and 0 <= cc < bsize and board[cr][cc] == other_color:
            iterated = True
            # print(cr, cc)
            tiles.add((cr, cc))
            cr += rstep
            cc += cstep
        if cr < 0 or cr == bsize or cc < 0 or cc == bsize or board[cr][cc] != cinv(other_color) or not iterated:
            pass
        else:
            # print(tiles)
            # print(board[cr][cc])
            # print(cr, cc)
            all_brackets.update(tiles)
    return all_brackets


def make_move(board, color, move):
    pieces = get_bracket_indices(board, move[0], move[1], cinv(color))
    for r, c in pieces:
        # board[idx] = color
        board[r][c] = color


def next_player(board, prev_player):
    p1_movs = legal_moves(board, cinv(prev_player))
    if len(p1_movs) == 0:
        p2_movs = legal_moves(board, prev_player)
        if len(p2_movs) == 0:
            return None
        return prev_player
    return cinv(prev_player)


# @cacher_tupleize
def check_direction(board, color, r, c, xstep, ystep):
    # if we didn't do this then it would start by checking an empty space
    r += xstep
    c += ystep
    iterated = False
    while 0 < r < bsize and 0 < c < bsize and board[r][c] == cinv(color):
        iterated = True
        r += xstep
        c += ystep
    if r < 0 or r == bsize or c < 0 or c == bsize or not iterated:
        return False
    return board[r][c] == color
