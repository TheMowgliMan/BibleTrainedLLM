CC :=

WARNINGS := -fsanitize=undefined -Wall -Werror
CFLAGS := -O3 -fvect-cost-model=dynamic -march=native $(WARNINGS)
SOFLAGS := -fPIC -c $(CFLAGS)
LDFLAGS := -shared -o libai-matrix.so

CC := gcc

OBJFILES = matrix_math.o

phony: all
all: matrix_math.o
	$(CC) $(LDFLAGS) $(OBJFILES)

phony: run
run: matrix_math.o
	$(CC) $(LDFLAGS) $(OBJFILES)
	python3 main.py

phony: matrix_math.o
matrix_math.o: lut.h
	$(CC) $(SOFLAGS) matrix_math.c -o matrix_math.o

phony: lut.h
lut.h:
	python3 lut_gen.py
