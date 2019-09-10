#!/usr/bin/env python3
"""Run an Othello game of Strategy vs RandomStrategy"""

import os
import signal
import sys
import importlib
from multiprocessing import Process

from Othello_Core import *
from ai import get_move, random
from helpers import *
from heuristics import count_colors
from helpers import to_tournament_format, to_tournament_move, from_tournament_move

TIMEOUT = 1


def main():
    global p1, p2
    board = array.array('B', [EMPTY] * 64)
    board[0o33] = BLACK
    board[0o44] = BLACK
    board[0o34] = WHITE
    board[0o43] = WHITE
    # we are blac, rnadom is white
    player = WHITE
    while Node(board, player).moving_plr is not None:
        # player = next_player(board, player)
        player = Node(board, player).moving_plr
        if player == BLACK:
            actual_move = run_a_strategy(board, player, p1)
            # actual_move = run_on_main_thread(board, player)
        elif player == WHITE:
            actual_move = run_a_strategy(board, player, p2)
        if actual_move not in Node(board, cinv(player)).legal_moves:
            raise RuntimeError(
                "Illegal move for player " + PLAYERS[player] + ": " + str(to_tournament_move(actual_move)))
        # print("Legal moves: " + str([to_tournament_move(move) for move in legal_moves(board, player)]))
        print("Move: " + str(to_tournament_move(actual_move)))
        make_move(board, player, actual_move)
        print_board(board)
    tmp = Node(board, BLACK)
    tmp.moving_plr = BLACK
    print("Black won!" if count_colors(tmp) > 0 else "Black lost!")


def run_on_main_thread(board, player):
    move = Value('i', 11)
    running = Value('i', 1)
    get_move(board, player, move, running)
    return from_tournament_move(move.value)


def run_them_on_main_thread(board, player):
    move = Value('i', 11)
    running = Value('i', 1)
    run_their_strategy(board, player, move)
    return from_tournament_move(move.value)


def run_a_strategy(board, color, strategy_func):
    move = Value('i', 11)
    proc = Process(target=strategy_func, args=(board, color, move))
    proc.start()
    # sleep(TIMEOUT)
    # sleep(0.1)
    try:
        proc.join(TIMEOUT)
    except:
        pass
    if proc.is_alive():
        print("TOO long.")
        #os.kill(proc.pid, signal.SIGKILL)
        proc.terminate()
        proc.is_alive()
    proc.terminate()
    proc.join(timeout=0)
    # actual_move = (move.value // 10 - 1, move.value % 10 - 1)
    actual_move = from_tournament_move(move.value)
    return actual_move


def run_our_strategy(board, color, move):
    runnin = Value('i', 1)
    get_move(board, color, move, runnin)
    print("DON GET MOV")


def run_their_strategy(board, color, move):
    runnin = Value('i', 1)
    # from other_strategy import Strategy
    mod = importlib.import_module(their_strat)
    s = mod.Strategy()
    s.best_strategy(to_tournament_format(board), TO_TOURNAMENT[color], move, runnin)
    print("DON GET MOV")


def run_their_strategy2(board, color, move):
    runnin = Value('i', 1)
    # from other_strategy import Strategy
    mod = importlib.import_module(their_strat2)
    s = mod.Strategy()
    s.best_strategy(to_tournament_format(board), TO_TOURNAMENT[color], move, runnin)
    print("DON GET MOV")


def run_random_strategy(board, color, move, modname=None):
    mv = random(board, color)
    move.value = to_tournament_move(mv)
    # move.value = (mv[0] + 1) * 10 + mv[1] + 1


#p1 = run_our_strategy
p1 = run_their_strategy
p2 = run_their_strategy2
# p2 = run_random_strategy

their_strat = "goodmemory" if len(sys.argv) <= 1 else sys.argv[1]
their_strat2 = "goodmemory" if len(sys.argv) <= 2 else sys.argv[2]

if __name__ == '__main__':
    main()
