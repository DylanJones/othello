#define BOARD_SIZE 64

inline int check_direction(unsigned char* board, char color, char r, char c, char rstep, char cstep);

char get_legal_moves(unsigned char* board, char color, unsigned char* output) {
    int numMoves = 0;
    for (int i = 0; i < BOARD_SIZE; i++) {
       int r = i / 8;
       int c = i % 8;
        if (board[i] == 0) {
            for (int rS = -1; rS <= 1; rS++) {
                for (int cS = -1; cS <= 1; cS++) {
                    if (rS == 0 && cS == 0) {
                        continue;
                    }
                    if (check_direction(board, color, r, c, rS, cS) && (numMoves == 0 || output[numMoves-1] != i) && numMoves < BOARD_SIZE) {
                        output[numMoves] = check_direction(board, color, r, c, rS, cS);
                        //output[numMoves] = i;
                        numMoves++;
                    }
                }
            }
        }
    }
    return (char)numMoves;
}
inline char cinv(char color){
    if (color == 1) {
        return 2;
    } else {
        return 1;
    }
}

inline int check_direction(unsigned char* board, char color, char r, char c, char rstep, char cstep) {
    r += rstep;
    c += cstep;
    bool iterated = false;
    while (0 <= r && r < 8 && c >= 0 && c < 8 && board[r*8+c] == cinv(color)) {
        iterated = true;
        r += rstep;
        c += cstep;
    }
    if (r < 0 || r >= 8 || c < 0 || c >= 8 || !iterated) {
        return 0;
    }
    return (board[r*8+c] == color) ? 1 : 0;
}
/*def legal_moves(board, color):
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

# @cacher_tupleize
def check_direction(board, color, i, direction):
    raise NotImplementedError("BORK")
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


@cacher_tupleize
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
    return all_brackets*/
