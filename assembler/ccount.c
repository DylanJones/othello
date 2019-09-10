#define OP_OVERALL_HEURISTIC 0
#define OP_COUNT_COLOR 1
#define OP_WEIGHT_MATRIX 2
#define OP_FRONTIER 3

#define EMPTY 0
#define BLACK 1
#define WHITE 2

int heuristic(unsigned char *board, char color) {
            int total = 0;
            for (int i = 0; i < 64; i++) {
                if (board[i] == color) {
                    total += 1;
                } else if (board[i] == ((color == BLACK) ? WHITE : BLACK)) {
                    total -= 1;
                }
            }
            return total;
}
