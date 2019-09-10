#define EMPTY 0
#define BLACK 1
#define WHITE 2

unsigned long long zobrist(unsigned char *board, unsigned long long* blackBits, unsigned long long* whiteBits, unsigned long long initalHashValue) {
    unsigned long long output = initalHashValue;
    for (int i = 0; i < 64; i++) {
        if (board[i] == WHITE) {
            output ^= whiteBits[i];
        } else if (board[i] == BLACK) {
            output ^= blackBits[i];
        }
    }
    return output;
}
