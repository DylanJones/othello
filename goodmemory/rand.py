"""
Base class for Othello Core
Must be subclassed by student Othello solutions
"""

from .Othello_Core import *
from . import helpers
from . import ai
import random

# convert the "direction" to something useful
DIR_OFFSET = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1),
              UP_LEFT: (-1, -1), UP_RIGHT: (-1, 1), DOWN_LEFT: (1, -1), DOWN_RIGHT: (1, 1)}


class RandomStrategy(OthelloCore):
    def is_valid(self, move):
        """Is move a square on the board?"""
        return 11 <= move < 89

    def opponent(self, player):
        """Get player's opponent piece."""
        return BLACK if player == WHITE else WHITE

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        r = square // 10
        c = square % 10
        rstep, cstep = DIR_OFFSET[direction]
        r += rstep
        c += cstep
        iterated = False
        while 1 < r < 9 and 1 < c < 9 and board[r * 10 + c] == self.opponent(player):
            iterated = True
            r += rstep
            c += cstep
        if r < 0 or r == 8 or c < 0 or c == 8 or not iterated:
            return False
        # return board[r*10+c] == player
        return r * 10 + c

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        # print(self.legal_moves(player, board))
        return move in self.legal_moves(player, board)

    # Making moves

    def legal_moves(self, player, board):
        def check_direction(board, color, r, c, xstep, ystep):
            # if we didn't do this then it would start by checking an empty space
            r += xstep
            c += ystep
            iterated = False
            while r > 1 and r < 9 and c > 1 and c < 9 and board[r * 10 + c] == self.opponent(color):
                iterated = True
                r += xstep
                c += ystep
            if r < 1 or r == 9 or c < 1 or c == 9 or not iterated:
                return False
            return board[r * 10 + c] == color
            # return board[r][c] == color

        moves = []
        for idx, spot in enumerate(board):
            # for c, spot in enumerate(row):
            r = idx // 10
            c = idx % 10
            if spot == EMPTY:  # it might be a legal move
                # check all directions
                for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if check_direction(board, player, r, c, *direction):
                        moves.append(idx)
                        break
        return moves

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        return len(self.legal_moves(player, board)) > 0

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.any_legal_move(self.opponent(prev_player), board):
            return self.opponent(prev_player)
        elif self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def score(self, player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        n = 0
        opp = self.opponent(player)
        # for r in board:
        for cell in board:
            if cell == player:
                n += 1
            elif cell == opp:
                n -= 1
        return n

    # STRATEGIES

    def best_strategy(self, board, player, best_move, still_running):
        """
        :param board: a length 100 list representing the board state
        :param player: WHITE or BLACK
        :param best_move: shared multiptocessing.Value containing an int of
                the current best move
        :param still_running: shared multiprocessing.Value containing an int
                that is 0 iff the parent process intends to kill this process
        :return: best move as an int in [11,88] or possibly 0 for 'unknown'
        """
        # print(board)
        # return self.lookahead_3(player, board)
        twoD = from_tournament_format(board)
        # mv = ai.get_move(twoD, player, best_move, still_running)
        mv = ai.random(twoD, player)
        # if mv is None:
        #    print("BAD BAD BAD")
        #    exit()
        #    return -12
        intm = (mv[0] + 1) * 10 + mv[1] + 1
        best_move.value = intm
        return intm


def from_tournament_format(board):
    """Take a "tournament format" (board that is too big with ? in it) and convert it to a 2D board"""
    nb = []
    for r in range(1, 9):
        nr = []
        for c in range(1, 9):
            nr.append(board[r * 10 + c])
        nb.append(nr)
    return nb


def to_tournament_format(board):
    """Take a normal 2D board and convert it to tournament format"""
    nb = ["?"] * 89
    for r in range(8):
        for c in range(8):
            nb[(r + 1) * 10 + c + 1] = board[r][c]
    return nb
