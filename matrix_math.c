#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "./lut.h"

#define PROC_RADIUS 16

inline int8_t __attribute__((always_inline)) lut_add(int8_t x, int8_t y)
{
    return add_tbl[(uint8_t)x * 256 + (uint8_t)y];
}

inline int64_t __attribute__((always_inline)) llclamp(int64_t n, int64_t min, int64_t max)
{
    const int64_t m = n < min ? min : n;
    return m > max ? max : m;
}

inline uint8_t __attribute__((always_inline)) cclamp(int8_t n, int8_t min, int8_t max)
{
    const int8_t m = n < min ? min : n;
    return m > max ? max : m;
}

void coladd_different_matrices(int8_t *restrict buf, int8_t *restrict x, int8_t *restrict y, uint64_t xlen, uint64_t ylen)
{
    int64_t tmplen = PROC_RADIUS * 2;
    int8_t *tmpmem = (int8_t*)malloc(tmplen * sizeof(int8_t));

    for (int64_t i = 0; i < xlen; i++)
    {
        memset(tmpmem, 0, tmplen * sizeof(int8_t));
        for (int64_t k = -1 * PROC_RADIUS; k < PROC_RADIUS; k++)
        {
            uint64_t tmpidx = llclamp(k + PROC_RADIUS, 0, tmplen);
            uint64_t yidx = llclamp(i + k, 0, ylen);

            tmpmem[tmpidx] = cclamp(lut_add(llabs(k) * -1, x[i] + y[yidx]), -127, 127);
        }

        buf[i] = 0;
        for (uint64_t k = 0; k < (2 * PROC_RADIUS); k++)
            buf[i] += tmpmem[k];
    }

    free(tmpmem);
}
