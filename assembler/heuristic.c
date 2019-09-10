#define OP_OVERALL_HEURISTIC 0
#define OP_COUNT_COLOR 1
#define OP_WEIGHT_MATRIX 2
#define OP_FRONTIER 3

#define EMPTY 0
#define BLACK 1
#define WHITE 2

int heuristic(unsigned char *board, char color, char *weightMatrix, int numLegalMoves, int opMode) {
    switch (opMode) {
        case OP_OVERALL_HEURISTIC: {
            //int frontierSquaresUs = heuristic(board, color, weightMatrix, numLegalMoves, OP_FRONTIER);
            //int frontierSquaresThem = heuristic(board, ((color == BLACK) ? WHITE : BLACK), weightMatrix, numLegalMoves,
            //                                    OP_FRONTIER);
            int weightMatrixScore = heuristic(board, color, weightMatrix, numLegalMoves, OP_WEIGHT_MATRIX);
            //int overallScore = ((frontierSquaresThem - frontierSquaresUs) * 0.5 + numLegalMoves * 2 +
            //                    weightMatrixScore * 10);
            int overallScore = (numLegalMoves * 2 + weightMatrixScore * 10);
            return overallScore;
        }
        case OP_COUNT_COLOR: {
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
        case OP_WEIGHT_MATRIX: {
            int total = 0;
            for (int i = 0; i < 64; i++) {
                if (board[i] == color) {
                    total += weightMatrix[i];
                } else if (board[i] == ((color == BLACK) ? WHITE : BLACK)) {
                    total -= weightMatrix[i];
                }
            }
            return total;
        }
        case OP_FRONTIER: {
            int total = 0;
            for (int r = 0; r < 8; r++) {
                for (int c = 0; c < 8; c++) {
                    if (board[r*8+c] == EMPTY) {
                    for (int rS = -1; rS <= 1; rS++) {
                        for (int cS = -1; cS <= 1; cS++) {
                            if (r + rS >= 0 && r + rS < 8 && c + cS >= 0 && c + cS < 8 && (rS != 0 || cS != 0)) {
                                int i = (r + rS) * 8 + c + cS;
                                if (board[i] == color) {
                                    total += 1;
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
            return total;
        }
        default:
            return -12345678;
    }
}
