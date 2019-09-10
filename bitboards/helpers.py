#!/usr/bin/env python3
from Othello_Core import OUTER
from Othello_Core import BLACK as t_b
from Othello_Core import WHITE as t_w
from Othello_Core import EMPTY as t_e

# EMPTY, BLACK, WHITE = '.', '@', 'o'
# EMPTY, BLACK, WHITE = b'.', b'@', b'o'
EMPTY, BLACK, WHITE = 0, 1, 2
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
PIECES = {BLACK: '@', WHITE: 'o', EMPTY: '.'}

TO_TOURNAMENT = {BLACK: t_b, WHITE: t_w, EMPTY: t_e}
FROM_TOURNAMENT = {y: x for x, y in TO_TOURNAMENT.items()}

NEGATIVE_INF = -(2 ** 80)
POSITIVE_INF = 2 ** 80

def to_tournament_move(move):
    # return (move[0] + 1) * 10 + move[1] + 1
    return (move // 8 + 1) * 10 + move % 8 + 1


def from_tournament_move(move):
    return (move // 10 - 1) * 8 + (move % 10 - 1)


def from_tournament_format(board):
    """Take a "tournament format" (board that is too big with ? in it) and convert it to a 2D board"""
    # return array.array('B', [FROM_TOURNAMENT[x] for x in board if x != OUTER])
    black = 0
    white = 0
    i = 0
    for piece in board:
        if piece != OUTER:
            if piece == TO_TOURNAMENT[BLACK]:
                black |= 1 << i
            elif piece == TO_TOURNAMENT[WHITE]:
                white |= 1 << i
            i += 1
    return black, white


def to_tournament_format(black, white):
    """Take a normal 2D board and convert it to tournament format"""
    nb = ["?"] * 100
    for r in range(8):
        for c in range(8):
            if (black << (r*8+c)) & 1:
                nb[(r+1)*10+c+1] = TO_TOURNAMENT[BLACK]
            elif (white << (r*8+c)) & 1:
                nb[(r+1)*10+c+1] = TO_TOURNAMENT[WHITE]
            else:
                nb[(r+1)*10+c+1] = TO_TOURNAMENT[EMPTY]
    return nb


def print_board(black, white):
    for r in range(8):
        print("\x1b[4m", end='')
        for c in range(8):
            if (black >> (r*8+c)) & 1:
                print(PIECES[BLACK], end='|')
            elif (white >> (r*8+c)) & 1:
                print(PIECES[WHITE], end='|')
            else:
                print(PIECES[EMPTY], end='|')
        print('\x1b[0m')
    print()

def cinv(c):
    """Color invert - change the color to the other color"""
    return WHITE if c == BLACK else BLACK

def legal_moves(us, them):
    # mask out edges
    mask = 0x7E7E7E7E7E7E7E7E & them
    return ((parital_compute_move(us, mask, 1) # horizontal
		| parital_compute_move(us, them, 8)  # vertical
		| parital_compute_move(us, mask, 7)  # diagonals
		| parital_compute_move(us, mask, 9)) # other diagonal
                & ~(us|them)) # only allow empty squares


def parital_compute_move(us, mask, dir):
    # algorithim that makes sense
    # print("MASK:")
    # print_board(mask, 0)
    flip = (((us << dir) | (us >> dir)) & mask)
    # print_board(flip, 0)
    flip |= (((flip << dir) | (flip >> dir)) & mask)
    # print_board(flip, 0)
    flip |= (((flip << dir) | (flip >> dir)) & mask)
    # print_board(flip, 0)
    flip |= (((flip << dir) | (flip >> dir)) & mask)
    # print_board(flip, 0)
    flip |= (((flip << dir) | (flip >> dir)) & mask)
    # print_board(flip, 0)
    flip |= (((flip << dir) | (flip >> dir)) & mask)
    # print_board(flip, 0)
    # print_board(0, (flip << dir) | (flip >> dir))
    return (flip << dir) | (flip >> dir)
    # kogge-stone algorithim?
    #dir2, dir4 = dir << 1, dir << 2
    #flip_l = us | (mask & (us << dir))
    #flip_r = us | (mask & (us >> dir))
    #mask_l  = mask & (mask << dir)
    #mask_r  = mask & (mask >> dir)
    #flip_l |= mask_l & (flip_l << dir2)
    #flip_r |= mask_r & (flip_r >> dir2)
    #mask_l &= (mask_l << dir2)
    #mask_r &= (mask_r >> dir2)
    #flip_l |= mask_l & (flip_l << dir4)
    #flip_r |= mask_r & (flip_r >> dir4)
    #return ((flip_l & mask) << dir) | ((flip_r & mask) >> dir)

def get_flips(us, them, bit_idx):
    mask = 0x7E7E7E7E7E7E7E7E & them
    us = (1 << bit_idx) # the moving piece
    # calc all flips from piece
    flips = flipcompute_plus(us, mask, 1)
    if not (flips & us):
        flips = 0
    tmp = flipcompute_minus(us, mask, 1)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_plus(us, them, 8)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_minus(us, them, 8)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_plus(us, mask, 7)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_minus(us, mask, 7)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_plus(us, mask, 9)
    if tmp & us:
        flips |= tmp
    tmp = flipcompute_minus(us, mask, 9)
    if tmp & us:
        flips |= tmp
    return flips
    #flips = parital_compute_move(us, mask, 1) \
    #      | parital_compute_move(us, them, 8) \
    #      | parital_compute_move(us, mask, 7) \
    #      | parital_compute_move(us, mask, 9)

def flipcompute_plus(us, mask, dir):
    flip = ((us << dir) & mask)
    flip |= ((flip << dir) & mask)
    flip |= ((flip << dir) & mask)
    flip |= ((flip << dir) & mask)
    flip |= ((flip << dir) & mask)
    flip |= ((flip << dir) & mask)
    return (flip << dir)

def flipcompute_minus(us, mask, dir):
    flip = ((us >> dir) & mask)
    flip |= ((flip >> dir) & mask)
    flip |= ((flip >> dir) & mask)
    flip |= ((flip >> dir) & mask)
    flip |= ((flip >> dir) & mask)
    flip |= ((flip >> dir) & mask)
    return (flip >> dir)



def next_player(board, prev_player):
    p1_movs = legal_moves(board, cinv(prev_player))
    if len(p1_movs) == 0:
        p2_movs = legal_moves(board, prev_player)
        if len(p2_movs) == 0:
            return None
        return prev_player
    return cinv(prev_player)


def zobrist(board, moving_plr):
    h = 0 if moving_plr == BLACK else plr_xor
    # h = 0
    for i, elem in enumerate(board):
        if elem == BLACK:
            h ^= z1[i]
        elif elem == WHITE:
            h ^= z2[i]
    return h


# transposition table format:
# key: zobrsist hash of board
# value: a tuple with elements...
# 0 - during the last run, the depth searched down from this node
# 1 - during the last run, the minimax score assigned to this node

# screw this LRU junk - let's make it UNLIMITED SIZE
cache = {}
ncache = {}
hits = 0
misses = 0


def transposition_lookup(board, moving_plr):
    global hits, misses
    hsh = zobrist(board, moving_plr)
    if hsh in cache:
        # if board != cache[hsh][2]:
        #     raise RuntimeError("HAS HIS BAAAAAAD")
        hits += 1
        return cache[hsh]
    misses += 1
    return None


def transposition_add(board, moving_plr, depth, score):
    # print(f"Hash size: {len(cache)}")
    hsh = zobrist(board, moving_plr)
    # if hsh in cache:
    #     # print(f"Updating cache: had depth {cache[hsh][0]}, new depth {depth}")
    #     # if cache[hsh]
    #     if cache[hsh][0] >= depth:
    #         if cache[hsh][1] != score:
    #             print(f"Old score: {cache[hsh][1]}, new: {score}")
    cache[hsh] = (depth, score)


# negatrans format:
# 0 - depth
# 1 - value
# 2 - type: one of (0-exact, 1-lower bound, 2-upper bound)

def negatrans_lookup(board, moving_plr):
    global hits, misses
    hsh = zobrist(board, moving_plr)
    if hsh in ncache:
        hits += 1
        return ncache[hsh]
    misses += 1
    return None


def negatrans_add(board, moving_plr, depth, score, node_type):
    hsh = zobrist(board, moving_plr)
    ncache[hsh] = (depth, score, node_type)


def pStat():
    print(f"Hits: {hits}, misses: {misses}")


