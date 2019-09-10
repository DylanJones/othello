#!/usr/bin/env python3
import importlib
import dispy
from subprocess import check_output
import multiprocessing
import pickle

from helpers import *
import ai
import cfunc_caller
import helpers
import heuristics
import machine_code
import Othello_Core
import random


def djones_ai_wrapper(board, player, depth):
    djones = importlib.import_module('goodmemory.ai')
    return djones.alphabeta(board, player, NEGATIVE_INF, POSITIVE_INF, player, depth)[1]


def duv_ai_wrapper(board, player, depth):
    duv = importlib.import_module('students.duv.strategy')
    s = duv.Strategy()
    tboard = to_tournament_format(board)
    spots_left = set(x for x in duv.sq if tboard[x] == TO_TOURNAMENT[EMPTY])
    node = [0, tboard, TO_TOURNAMENT[player], spots_left, [], None,
            duv.find_all_brackets(tboard, TO_TOURNAMENT[player], spots_left, s), -1, -1,
            TO_TOURNAMENT[player] + ''.join(tboard)]
    badmove = duv.abprune(node, s, 0, depth-1, s.tMatrix, -duv.inf, duv.inf, TO_TOURNAMENT[player], dict())[1]
    return from_tournament_move(badmove)



STEP_SIZE = 0.00001
INITAL_RANDOM_MOVES = 8
NUM_SIMULATIONS = 1000


# DISPY_HOSTNAMES = ["borg1.csl.tjhsst.edu", "borg3.csl.tjhsst.edu", "borg4.csl.tjhsst.edu", "borg40.csl.tjhsst.edu",
#                    "gandalf.csl.tjhsst.edu", "skynet.karel.pw"] + ["hpc" + str(i) + ".csl.tjhsst.edu" for i in
#                                                                    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12]]
# DISPY_HOSTNAMES = ["skynet.karel.pw"]
# DISPY_IPS = [check_output(f"host {hostname} | grep -oP '(?<=address )[0-9.]+$'", shell=True).decode(
#     "UTF-8").strip() for hostname in DISPY_HOSTNAMES]
# print(f"Nodes: {DISPY_IPS}")


def play_random(board, moving_plr, num_moves):
    """Take board, and play a random game for # moves"""
    import helpers, random
    for i in range(num_moves):
        if moving_plr is None:
            return board, None
        move = random.choice(helpers.legal_moves(board, moving_plr))
        helpers.make_move(board, moving_plr, move)
        moving_plr = helpers.next_player(board, moving_plr)
    return board, moving_plr


def run_game(weights):
    """Run a game of the current AI vs the old AI"""
    import helpers, random, heuristics
    helpers.SQUARE_WEIGHTS = weights
    black_moves = []
    white_moves = []
    black_ai = duv_ai_wrapper
    white_ai = djones_ai_wrapper
    # keep track of whether or not we switched the starting order
    black_ai_type = 'training'
    if random.random() < 0.5:
        black_ai, white_ai = white_ai, black_ai
        black_ai_type = 'nottraining'
    board = array.array('B', [helpers.EMPTY] * 64)
    board[0o33] = helpers.BLACK
    board[0o44] = helpers.BLACK
    board[0o34] = helpers.WHITE
    board[0o43] = helpers.WHITE
    player = helpers.BLACK
    PLR2AI = {helpers.BLACK: black_ai, helpers.WHITE: white_ai}
    player = play_random(board, player, 8)[1]
    while player is not None:
        # depth of 2, we want this to be FAST
        move = PLR2AI[player](board, player, 2)
        if move not in helpers.legal_moves(board, player):
            raise RuntimeError(f"Illegal move for {helpers.PLAYERS[player]}: {move}")
        if player == BLACK:
            black_moves.append(move)
        else:
            white_moves.append(move)
        helpers.make_move(board, player, move)
        player = helpers.next_player(board, player)
        # print_board(board)
        # print()
    if black_ai_type == 'training':
        didWin = heuristics.count_colors(board, BLACK) > 0
    else:
        didWin = heuristics.count_colors(board, WHITE) > 0
    if heuristics.count_colors(board, BLACK) > 0:
        return black_moves, white_moves, heuristics.count_colors(board, BLACK), didWin
    elif heuristics.count_colors(board, WHITE) > 0:
        return white_moves, black_moves, heuristics.count_colors(board, WHITE), didWin
    else:  # it was a tie
        return [], [], 0, False
    # if black_ai_type == 'training':
    #     return heuristics.count_colors(board, helpers.BLACK)
    # else:
    #     return heuristics.count_colors(board, helpers.WHITE)


def eval_weights_dispy(oldweights, newweights):
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    def callback(job):
        nonlocal finished
        finished += 1
        print(f'\rSimulations finished: {finished}', end='')

    cluster = dispy.JobCluster(run_game, nodes=DISPY_IPS,
                               depends=[ai, cfunc_caller, helpers, heuristics, machine_code, __file__, Othello_Core,
                                        play_random],
                               callback=callback, ip_addr='198.38.22.6', pulse_interval=2, reentrant=True,
                               ping_interval=10)
    # ping_interval=10, loglevel=dispy.logger.DEBUG)
    cluster.print_status()
    intermediate_arr = []
    results = []
    finished = 0

    for _ in range(NUM_SIMULATIONS):
        # intermediate_arr.append(pool.apply_async(run_game, callback=callback))
        intermediate_arr.append(cluster.submit(oldweights, newweights))
    # time.sleep(5)
    cluster.print_status()
    for i, job in enumerate(intermediate_arr):
        # results.append(res.get())
        # print(f'\rSimulations finished: {i}', end='')
        results.append(job())
        if job.status == dispy.DispyJob.Finished:
            # print("Successful job!")
            pass
        else:
            print(job.exception)
    print()
    print(results)
    print(f"Won {sum(x>0 for x in results)} games ({sum(x>0 for x in results)/NUM_SIMULATIONS*100}%)")
    print(f'Lost {sum(x<0 for x in results)} games ({sum(x<0 for x in results)/NUM_SIMULATIONS*100}%)')
    cluster.print_status()


def run_many_games(newweights):
    global pool

    def callback(*_, **__):
        nonlocal finished
        finished += 1
        print(f'\rSimulations finished: {finished}', end='')

    intermediate_arr = []
    results = []
    finished = 0

    for _ in range(NUM_SIMULATIONS):
        intermediate_arr.append(pool.apply_async(run_game, args=(newweights,), callback=callback))
    for i, res in enumerate(intermediate_arr):
        results.append(res.get())
    print()
    # print(results)
    # print(f"Won {sum(x>0 for x in results)} games ({sum(x>0 for x in results)/NUM_SIMULATIONS*100}%)")
    # print(f'Lost {sum(x<0 for x in results)} games ({sum(x<0 for x in results)/NUM_SIMULATIONS*100}%)')
    # return sum(results)/NUM_SIMULATIONS
    return results


def train_weights():
    inital_weights = SQUARE_WEIGHTS
    new_weights = list(SQUARE_WEIGHTS)
    i = 0
    while True:
        results = run_many_games(new_weights)
        total_score = 0
        for goodmoves, badmoves, scoreAmount, didWin in results:
            total_score += scoreAmount * (1 if didWin else -1)
            for move in goodmoves:
                new_weights[move] += scoreAmount * STEP_SIZE
            for move in badmoves:
                new_weights[move] -= scoreAmount * STEP_SIZE
        print(f"Average score: {total_score/NUM_SIMULATIONS}")
        print(new_weights)
        with open(f"matrix_{i}.pkl", 'wb') as f:
            pickle.dump(new_weights, f)
        i += 1


if __name__ == '__main__':
    # print(f'Monte Carlo score: {eval_weights(helpers.SQUARE_WEIGHTS, helpers.SQUARE_WEIGHTS)}')
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    train_weights()
