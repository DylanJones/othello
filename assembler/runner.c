#include <stdio.h>
#include <time.h>
#include <stdlib.h>
//#include "legal_moves.c"
#include "legal_moves_inline.c"
#define NUMITER 500000

//unsigned char board[] = {0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0};

//unsigned char board[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
unsigned char board[] = {1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1};

int main(void) {
    unsigned char* b = board;
    unsigned char* scratch = (unsigned char*)malloc(sizeof(unsigned char) * 64);
    char player = 1;
    char res = get_legal_moves(b, player, scratch);
    printf("Result: %u\n", res);
    for (int i = 0; i < 64; i++) {
        printf("%u ", scratch[i]);
    }
    printf("\n");
    long double timeTotal = 0;
    clock_t start, end;
    for (int i = 0; i < NUMITER; i++) {
        start = clock();
        get_legal_moves(b, player, scratch);
        end = clock();
        timeTotal += (double)(end-start);
    }
    printf("Average time: %f\n", (double)(timeTotal / CLOCKS_PER_SEC / NUMITER * 100000));
}
