import sys

# We use error guards for silly people who run this without pytorch
try:
    import torch
    from torch import nn
except ModuleNotFoundError:
    sys.exit("This cannot be run without PyTorch installed!\nTry running 'pip3 install torch'")

try:
    from transformers import DebertaV2Tokenizer
except ModuleNotFoundError:
    sys.exit("This cannot be built without Transformers installed!\nTry running 'pip3 install transformers'")

try:
    import ctypes as c
except ModuleNotFoundError:
    sys.exit

try:
    import sentencepiece as spm
except ModuleNotFoundError:
    sys.exit("This cannot be built without SentencePiece installed!\nTry running 'pip3 install sentencepiece'")

import util

if __name__ == "__main__":
    tok = spm.SentencePieceProcessor()
    tok.load("homebrewModel.model")

    # encoded = tok.encode("Hello world!", out_type='immutable_proto')
    # for n in encoded.pieces:
    #     data = util.token_to_data(n.id, n.begin)
    #     print(n.id)
    #     print(data)
    #     print(util.data_to_token(data))

    while True:
        inp = input("?> ")
        if inp == "exit":
            break

        encoded = tok.encode(inp, out_type='immutable_proto')
        for n in encoded.pieces:
            data = util.token_to_data(n.id, n.begin)
            print(data)
else:
    sys.exit("This system does not support being run as an importable module at this time.")
