#define OP_OVERALL_HEURISTIC 0
#define OP_COUNT_COLOR 1
#define OP_WEIGHT_MATRIX 2
#define OP_FRONTIER 3

#define EMPTY 0
#define BLACK 1
#define WHITE 2

int heuristic(unsigned char *board, char color) {
    int total = 0;
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            if (board[r*8+c] == EMPTY) {
                for (int rS = -1; rS <= 1; rS++) {
                    for (int cS = -1; cS <= 1; cS++) {
                        if (r + rS >= 0 && r + rS < 8 && c + cS >= 0 && c + cS < 8 && (rS != 0 || cS != 0)) {
                            int i = (r + rS) * 8 + c + cS;
                            if (board[i] == color) {
                                total -= 1;
                                goto out;
                            } 
                        }
                    }
                }
out:
                continue;

            }
        }
    }
    color = ((color == BLACK) ? WHITE : BLACK);
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            if (board[r*8+c] == EMPTY) {
                for (int rS = -1; rS <= 1; rS++) {
                    for (int cS = -1; cS <= 1; cS++) {
                        if (r + rS >= 0 && r + rS < 8 && c + cS >= 0 && c + cS < 8 && (rS != 0 || cS != 0)) {
                            int i = (r + rS) * 8 + c + cS;
                            if (board[i] == color) {
                                total += 1;
                                goto out2;
                            }
                        }
                    }
                }
out2:
                continue;

            }
        }
    }
    return total;
}
