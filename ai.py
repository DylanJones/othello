#!/usr/bin/env python3
"""
This module contains the various decision making functions.
"""
from helpers import *
from heuristics import score
import machine_code
from random import choice, shuffle
import time


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


def delta_epsilon(node: Node, color, delta: int, epsilon: int, depth: int):
    global nNode
    if node.moving_plr is None or depth == 0:
        nNode += 1
        return score(node), None
    best = NEGATIVE_INF if node.moving_plr == color else POSITIVE_INF
    bestmv = None
    for move in node.legal_moves:
        board2 = copy_board(node.board)
        make_move(board2, node.moving_plr, move)
        node2 = Node(board2, node.moving_plr)
        # print(f"depth:{depth}, Original board:")
        # print_board(board)
        # print(f"{node.moving_plr} makes a move")
        # print_board(board2)
        mmx = delta_epsilon(node2, color, delta, epsilon, depth - 1)[0]
        # print(f"depth:{depth} delta: {delta} epsilon: {epsilon} mmx: {mmx}")
        # print_board(board2)
        if node.moving_plr == color:
            bestmv = bestmv if best > mmx else move
            best = max(best, mmx)
            delta = max(best, delta)
        else:
            best = min(best, mmx)
            epsilon = min(best, epsilon)
        if epsilon <= delta:  # alpha-beta cutoff
            break
    return best, bestmv


def alphabeta_memory(board, color, alpha, beta, moving_plr, depth):
    # print_board(board)
    global nNode
    if moving_plr is None or depth == 0:
        nNode += 1
        return score(board, color), None
    moves = legal_moves(board, moving_plr)
    nodes = []
    for move in moves:
        board2 = copy_board(board)
        make_move(board2, moving_plr, move)
        cval = transposition_lookup(board2, moving_plr)
        if cval is not None:
            nodes.append((cval[0], cval[1], move, board2))
        else:
            nodes.append((NEGATIVE_INF, NEGATIVE_INF, move, board2))
    nodes.sort(key=lambda x: x[1], reverse=True)
    best = NEGATIVE_INF if moving_plr == color else POSITIVE_INF
    bestmv = None
    for node in nodes:
        if node[0] < depth:
            mmx = alphabeta_memory(node[3], color, alpha, beta, next_player(node[3], moving_plr), depth - 1)[0]
            transposition_add(node[3], moving_plr, depth, mmx)
        else:
            # print('Hit')
            mmx = node[1]
        if moving_plr == color:
            bestmv = bestmv if best > mmx else node[2]
            best = max(best, mmx)
            alpha = max(best, alpha)
        else:
            best = min(best, mmx)
            beta = min(best, beta)
        if beta <= alpha:  # alpha-beta cutoff
            # print("alpha beta cutoff")
            break
    print(f'Depth: {depth}, heuristic: {score(board, color)}, minimax value: {best}')
    return best, bestmv


def negamax_ab(board, color, alpha, beta, moving_plr, depth):
    init_alpha = alpha
    ttval = negatrans_lookup(board, moving_plr)
    if ttval is not None and ttval[0] >= depth:
        if ttval[2] == FLAG_EXACT:
            return ttval[1]
        elif ttval[2] == FLAG_LOWER:
            alpha = max(alpha, ttval[1])
        elif ttval[2] == FLAG_UPPER:
            beta = min(beta, ttval[1])
    if depth == 0 or moving_plr is None:
        return score(board, color) * (1 if color == BLACK else -1)


def get_move(board, player, best_move, still_running):
    global nNode
    from ai_old import alphabeta as old_ab
    """Get the best move for specified player"""
    i = 1
    while still_running.value and i < 20:  # too much
        s = time.time()
        nNode = 0
        # mv = old_ab(board, player, i)
        # mv = delta_epsilon(board, player, NEGATIVE_INF, POSITIVE_INF, player, i)[1]
        node = Node(board, cinv(player))
        mv = delta_epsilon(node, player, NEGATIVE_INF, POSITIVE_INF, i)[1]
        # mv = alphabeta_memory(board, player, NEGATIVE_INF, POSITIVE_INF, player, i)[1]
        best_move.value = 12345
        print(f"nodes: {nNode}")
        print(f"cache: {len(cache)}")
        print(f"alphabeta: {time.time()-s} seconds for i={i}")
        pStat()
        jmv = to_tournament_move(mv)
        best_move.value = jmv
        i += 2 if i <= 4 else 1
    return mv


nNode = 0
if __name__ == '__main__':
    from ai_old import alphabeta as old_ab

    board = from_tournament_format(
        "???????????@@@@@...??.oo@@...??ooo@@@..??oo@o@@..??.oo@o@..??oo@@@@@.??...@@oo.??...@ooo.???????????")
    #board = from_tournament_format(
    #    "???????????....@...??..o@@...??.@@@@@@o??..@@o@o.??..o@@oo.??..o@@@o.??...@@@..??........???????????")
    for i in range(1, 9):
        nNode = 0
        s = time.time()
        # mv = delta_epsilon(board, BLACK, NEGATIVE_INF, POSITIVE_INF, BLACK, i)
        nod = Node(board, BLACK)
        mv = delta_epsilon(nod, BLACK, NEGATIVE_INF, POSITIVE_INF, i)
        e = time.time()
        print(f'alphabeta took {e-s} seconds for i={i}')
        print(f"nodes: {nNode}")
        print(f"cache: {len(cache)}")
        # nNode = 0
        # s = time.time()
        # mv = alphabeta_memory(board, BLACK, NEGATIVE_INF, POSITIVE_INF, BLACK, i)
        # e = time.time()
        # print(f'alphabeta_memory took {e-s} seconds for i={i}')
        # print(f"nodes: {nNode}")
        # print(f"cache: {len(cache)}")
        # nNode = 0
        # s = time.time()
        # mv = old_ab(board, BLACK, i - 1)
        # e = time.time()
        # print(f'alphabeta_old took {e-s} seconds for i={i}')
        # print(f"nodes: {nNode}")
        # print(f"cache: {len(cache)}")
