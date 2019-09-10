from helpers import *
from heuristics import count_colors
from array import array

STARTING_BOARD = array('B', [EMPTY] * 64)

STARTING_BOARD[0o33] = WHITE
STARTING_BOARD[0o44] = WHITE
STARTING_BOARD[0o34] = BLACK
STARTING_BOARD[0o43] = BLACK

blk_sym = '+'
wht_sym = '-'
ltr_to_col = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e':5, 'f':6, 'g':7, 'h':8}
plr_to_player = {'+': BLACK, '-': WHITE}

with open('outfile.txt', 'w') as outfile:
  with open('logbook.gam', 'r') as f:
    i=0
    for l1 in f:
    # l1 = f.readline()
      #print(f'l1:{l1}')
      moves = [l1[x:x+3] for x in range(0, l1.find(':'), 3)]
      bscore = [int(x) for x in l1.strip().split(' ')[1:]]
      bscore = bscore[0]
      #print(moves)
      #print(bscore)
      bcpy = copy_board(STARTING_BOARD)
      for move in moves:
        plr = plr_to_player[move[0]]
        col = ltr_to_col[move[1]]
        row = int(move[2])
        idx = (col-1)+(row-1)*8
        if idx not in legal_moves(bcpy, plr):
          print(f'{idx} Bad')
        make_move(bcpy, plr, idx)
        # print_board(bcpy)
        # print()
        outfile.write(''.join(str(x) for x in bcpy) + "," + str(bscore) + "\n")
      # print_board(bcpy)
      # print(moves)
      # print(count_colors(bcpy, BLACK))
      # print(bscore)
      if i % 100 == 0:
        print(f'{i}')
      i += 1
