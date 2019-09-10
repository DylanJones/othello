"""
Base class for Othello Core
Must be subclassed by student Othello solutions
"""

from Othello_Core import *
from helpers import *
import ai

# convert the "direction" to something useful
DIR_OFFSET = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1),
              UP_LEFT: (-1, -1), UP_RIGHT: (-1, 1), DOWN_LEFT: (1, -1), DOWN_RIGHT: (1, 1)}


class Strategy:
    def best_strategy(self, board, player, best_move, still_running):
        twoD = from_tournament_format(board)
        mv = ai.get_move(twoD, FROM_TOURNAMENT[player], best_move, still_running)
        if mv is None:
            print("BAD BAD BAD")
            exit()
            return -12
        intm = to_tournament_move(mv)
        best_move.value = intm
        return intm
