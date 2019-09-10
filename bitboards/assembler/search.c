#define EMPTY 0
#define BLACK 1
#define WHITE 2
#define BOARD_SIZE 64

inline int countColors(unsigned char *board, char color) {
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
inline int frontierSquares(unsigned char *board, char color) {
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
inline int checkDirection(unsigned char* board, char color, char r, char c, char rstep, char cstep);

inline char getLegalMoves(unsigned char* board, char color, unsigned char* output) {
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
                    if (checkDirection(board, color, r, c, rS, cS) && (numMoves == 0 || output[numMoves-1] != i) && numMoves < BOARD_SIZE) {
                        output[numMoves] = checkDirection(board, color, r, c, rS, cS);
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

inline int checkDirection(unsigned char* board, char color, char r, char c, char rstep, char cstep) {
    r += rstep;
    c += cstep;
    bool iterated = false;
    while (0 < r && r < 8 && c > 0 && c < 8 && board[r*8+c] == cinv(color)) {
        iterated = true;
        r += rstep;
        c += cstep;
    }
    if (r < 0 || r >= 8 || c < 0 || c >= 8 || !iterated) {
        return 0;
    }
    return (board[r*8+c] == color) ? 1 : 0;
}

inline int weightMatrix(unsigned char *board, char color, char *weightMatrix) {
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
/*inline unsigned long long zobrist(unsigned char *board, unsigned long long* blackBits, unsigned long long* whiteBits, unsigned long long initalHashValue) {
    unsigned long long output = initalHashValue;
    for (int i = 0; i < 64; i++) {
        if (board[i] == WHITE) {
            output ^= whiteBits[i];
        } else if (board[i] == BLACK) {
            output ^= blackBits[i];
        }
    }
    return output;
}*/
