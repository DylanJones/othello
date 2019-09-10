#!/usr/bin/env python3
from functools import lru_cache
from Othello_Core import OUTER
import array
import warnings
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

FLAG_LOWER, FLAG_UPPER, FLAG_EXACT = 1, 2, 0

# the square_weights from http://dhconnelly.com/paip-python/docs/paip/othello.html
# also happens to be the same one in othello_admin.py
SQUARE_WEIGHTS_OLD = [
    120, -20, 20, 5, 5, 20, -20, 120,
    -20, -40, -5, -5, -5, -5, -40, -20,
    20, -5, 15, 3, 3, 15, -5, 20,
    5, -5, 3, 3, 3, 3, -5, 5,
    5, -5, 3, 3, 3, 3, -5, 5,
    20, -5, 15, 3, 3, 15, -5, 20,
    -20, -40, -5, -5, -5, -5, -40, -20,
    120, -20, 20, 5, 5, 20, -20, 120,
]
# let's try modifying them to not put importance on the middle so we can focus on opening up our options
SQUARE_WEIGHTS = [
    35, -7, 4, 2, 2, 4, -7, 35,
    -7, -20, 0, 0, 5, 0, -20, -7,
    4, 0, 0, 0, 0, 0, 0, 4,
    2, 0, 0, 0, 0, 0, 0, 2,
    2, 0, 0, 0, 0, 0, 0, 2,
    4, 0, 0, 0, 0, 0, 0, 4,
    -7, -20, 0, 0, 0, 0, -20, -7,
    35, -7, 4, 2, 2, 4, -7, 35,
]

# random arrays
# z1, z2 = [int(random.random()*(2<<64)) for _ in range(64)]
z1 = [8659954393609752576, 8965948371027167232, 8223607566414987264, 5683414317467676672, 15021504696916344832,
      3285575905592272896, 12405934113292105728, 14792198880489099264, 11566765862981939200, 13354054981775230976,
      13452893006022250496, 366086618649978880, 5580919339304882176, 817173445631232000, 2829050999139960832,
      14904254464113764352, 12863389963850852352, 1428664302341623808, 11482914551567323136, 16962100657604571136,
      2775570736201838592, 2293014778132492288, 2812742723043780608, 10496812132233279488, 4106783031285643264,
      5887767676054593536, 10638447612355323904, 635376310806165504, 9757944913013927936, 2889527168558010368,
      12571942260317984768, 11922232533225355264, 1184455908293588992, 14288758704518146048, 7980843622115500032,
      12673713184237910016, 4170508080868720640, 11715684877207066624, 5875656083014084608, 15631573845712537600,
      17236903579809648640, 2774567329456556032, 13899445684074969088, 5574619111409383424, 15729945418380054528,
      10567629513364123648, 13798125425839421440, 13721475445287604224, 4866812821795532800, 9871799205200396288,
      15345988643706574848, 16404693265372485632, 9056633745033857024, 9294359629817626624, 3196233626188838912,
      16343253101121849344, 11572940326956959744, 11897078261909372928, 1265559827261704192, 18386638457879891968,
      1122146335471253504, 6624187648701376512, 6954249388685426688, 11962091518603548672]
z2 = [122396131168020480, 5598828686647588864, 2289128025341906944, 3894894488568963072, 14897094034504660992,
      10634020137052899328, 6529797070158671872, 16570011370128228352, 8029059210349363200, 14129749737073618944,
      12672381257652676608, 13540772201768073216, 12778394716863309824, 11601027141158088704, 18219699723229569024,
      109895667660187648, 6464667453714688000, 13904017103938476032, 1005594953465219072, 15637745252240508928,
      4057195751176804352, 16382347664937746432, 8847077602035931136, 2075395646177081344, 15018792526347495424,
      1549884970407051264, 18232264381638137856, 14170016906719053824, 1430528822921062400, 12281299541796116480,
      13522084499951542272, 8829965645864491008, 14426427542096826368, 586533761207005184, 17243867434894084096,
      502034036415393792, 11148387007056783360, 2620579092818534400, 2474868906912497664, 18125932184270637056,
      14623761845848438784, 13538351566004447232, 17320536853036679168, 5270589452972142592, 16786125046080147456,
      1239279439272224768, 6036842932985880576, 16351737113862254592, 530707297401012224, 9951244556692566016,
      136093365316319232, 834376164935792640, 2065413665211035648, 17923624933607266304, 2781286490241632256,
      12131279078526453760, 6458969579160784896, 14184630078223282176, 6758316706779328512, 16023027521314318336,
      6368160618427305984, 3277264078235162624, 12644956400573353984, 7637980332416722944]

plr_xor = 34058210710748721152


def copy_board(board):
    # return [list(b) for b in board]
    # return list(board)
    return array.array('B', board)


def to_tournament_move(move):
    # return (move[0] + 1) * 10 + move[1] + 1
    return (move // 8 + 1) * 10 + move % 8 + 1


def from_tournament_move(move):
    return (move // 10 - 1) * 8 + (move % 10 - 1)


def from_tournament_format(board):
    """Take a "tournament format" (board that is too big with ? in it) and convert it to a 2D board"""
    return array.array('B', [FROM_TOURNAMENT[x] for x in board if x != OUTER])
    # nb = []
    # for r in range(1, 9):
    #     nr = []
    #     for c in range(1, 9):
    #         nr.append(board[r * 10 + c])
    #     nb.append(nr)
    # return nb


def to_tournament_format(board):
    """Take a normal 2D board and convert it to tournament format"""
    nb = ["?"] * 100
    for r in range(8):
        for c in range(8):
            nb[(r + 1) * 10 + c + 1] = TO_TOURNAMENT[board[r * 8 + c]]
    return nb


def cacher_tupleize(func):
    """Like LRU cache but always convert first arg to tuple"""
    cfunc = lru_cache(2 ** 24, True)(func)

    def f(lst, *args, **kwargs):
        # tpl = tuple(tuple(x) for x in lst)
        tpl = tuple(lst)
        # print(args, kwargs)
        return cfunc(tpl, *args, **kwargs)

    return f


def print_board(board):
    for r in range(8):
        print("\x1b[4m", end='')
        for c in range(8):
            print(PIECES[board[r * 8 + c]], end='|')
        print('\x1b[0m')
    print()
    # for r in board:
    #     print("\x1b[4m", end='')
    #     for c in r:
    #         print(c, end='|')
    #     print('\x1b[0m')
    # print()


def cinv(c):
    """Color invert - change the color to the other color"""
    return WHITE if c == BLACK else BLACK


@cacher_tupleize
def legal_moves(board, color):
    moves = []
    for i, cell in enumerate(board):
        if cell == EMPTY:
            if len(get_bracket_indices(board, i, cinv(color))) > 0:
                moves.append(i)
            # check directions
            # for direction in [-8, 8, 1, -1, -9, 9, -7, 7]:
            #     if check_direction(board, color, i, direction):
            #         print(f"loc: {i}, dir: {direction}")
            #         moves.append(i)
            #         break
    return moves
    # moves = []
    # for r, row in enumerate(board):
    #     for c, spot in enumerate(row):
    #         if spot == '.':  # it might be a legal move
    #             # check all directions
    #             for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
    #                 if check_direction(board, color, r, c, *direction):
    #                     moves.append((r, c))
    #                     break
    # return moves


# @cacher_tupleize
def get_bracket_indices(board, pos, other_color):
    # this gets really inelegant without using r,c
    all_brackets = set()
    for rstep, cstep in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        # cr, cc = r, c
        cr, cc = pos // 8, pos % 8
        tiles = {(cr * 8 + cc)}
        cr += rstep
        cc += cstep
        iterated = False
        while 0 <= cr < 8 and 0 <= cc < 8 and board[cr * 8 + cc] == other_color:
            iterated = True
            tiles.add((cr * 8 + cc))
            cr += rstep
            cc += cstep
        if cr < 0 or cr == 8 or cc < 0 or cc == 8 or board[cr * 8 + cc] != cinv(other_color) or not iterated:
            pass
        else:
            all_brackets.update(tiles)
    return all_brackets


def make_move(board, color, move):
    pieces = get_bracket_indices(board, move, cinv(color))
    for idx in pieces:
        board[idx] = color
        # board[r][c] = color


def next_player(board, prev_player):
    p1_movs = legal_moves(board, cinv(prev_player))
    if len(p1_movs) == 0:
        p2_movs = legal_moves(board, prev_player)
        if len(p2_movs) == 0:
            return None
        return prev_player
    return cinv(prev_player)


# @cacher_tupleize
def check_direction(board, color, i, direction):
    raise NotImplementedError("BORK")
    # if we didn't do this then it would start by checking an empty space
    # i += direction
    # iterated = False
    # while 0 <= i < 64 and board[i] == cinv(color):
    #     iterated = True
    #     i += direction
    # if i < 0 or i >= 64 or not iterated:
    #     return False
    # return board[i] == color
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


# Now to override with C vesrions!
try:
    from machine_code import legal_moves
    from machine_code import zobrist
    pass
except RuntimeError:
    warnings.warn("Failed to import machine code - falling back to slow python-only implementation", RuntimeWarning)
