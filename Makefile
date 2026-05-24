ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

CC :=

WARNINGS := -fsanitize=undefined -Wall -Werror
CFLAGS := -O3 -fvect-cost-model=dynamic -march=native $(WARNINGS)
SOFLAGS := -fPIC -c $(CFLAGS)
LDFLAGS := -shared -o libai-matrix.so

CC := gcc

VENVDIR := homebrewLLMModel
INSTALLDIR := $(HOME)/opt/homebrewLLM

VPY := $(HOME)/.venvs/$(VENVDIR)/bin/python3

OBJFILES = matrix_math.o
VOCABFILE :=

INSTALLCOM := alias homebrewLLM='$(INSTALLDIR)/homebrewLLM.sh $(INSTALLDIR) $(VENVDIR)'

.PHONY: run
run: all
	$(ROOT_DIR)/homebrewLLM.sh $(ROOT_DIR) $(VENVDIR)

.PHONY: all
all: scripts/shell/.deps-obtained matrix_math.o
	$(CC) $(LDFLAGS) $(OBJFILES)

.PHONY: install
install:
	mkdir -p $(INSTALLDIR)
	echo "$(INSTALLCOM)" >> $(HOME)/.bashrc
	source $(HOME)/.bashrc

.PHONY: scripts/shell/.deps-obtained
scripts/shell/.deps-obtained:
	scripts/shell/install-deps.sh $(VENVDIR)

.PHONY: matrix_math.o
matrix_math.o: lut.h
	$(CC) $(SOFLAGS) matrix_math.c -o matrix_math.o

.PHONY: lut.h
lut.h:
	export PYTHONPATH="$(ROOT_DIR)"; \
	python3 scripts/py/lut_gen.py

.PHONY: generate-vocabulary
generate-vocabulary: homebrewModel.model

.PHONY: homebrewModel.model
homebrewModel.model:
	export PYTHONPATH="$(ROOT_DIR):$(ROOT_DIR)/scripts/py:$$PYTHONPATH"; \
	. $(HOME)/.venvs/$(VENVDIR)/bin/activate; \
	$(VPY) scripts/py/generate-vocabulary.py training-data/test-vocabulary.txt; \
	deactivate
