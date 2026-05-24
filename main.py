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

def dprint(msg: str):
    print(f"[ DEBUG ] {msg}")

import util
import struct

# To make a buffer:
# size = <size>
# buf = ctypes.create_string_buffer(<data>, size=size)
# ...<do stuff>...
# pba = ctypes.string_at(buf, size=4000)
# tup = struct.unpack(<format string>, pba)

if __name__ == "__main__":
    dprint("Loading SentencePiece model...")
    tok = spm.SentencePieceProcessor()
    tok.load("homebrewModel.model")

    dprint("Loading 'libai-matrix.so'...")
    mtrx = c.CDLL("./libai-matrix.so")

    dprint("Initializing shared libraries...")


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

        rows = [[], [], [], [], [], [], [], []] # Absolute programmergore

        encoded = tok.encode(inp, out_type='immutable_proto')
        for n in encoded.pieces:
            data = util.token_to_data(n.id, n.begin)

            rows[0].append(data[0])
            rows[1].append(data[1])
            rows[2].append(data[2])
            rows[3].append(data[3])
            rows[4].append(data[4])
            rows[5].append(data[5])
            rows[6].append(data[6])
            rows[7].append(data[7])
else:
    sys.exit("This system does not support being run as an importable module at this time.")
