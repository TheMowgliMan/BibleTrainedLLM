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

def __pad(list_, len_):
    while len(list_) < len_:
        list_.insert(0, 0)

def __pass_list_as_array(list_, arrsz=2048):
    zed = [0] * arrsz
    arr = (c.c_int8 * arrsz)()

    for i, k in enumerate(list_):
        arr[i] = k

    return arr

def __pass_array_as_list(arr_, arrsz=2048):
    zed = [0] * arrsz

    for i in range(arrsz):
        zed[i] = arr_[i]

    return zed

def __malloc(arrsz):
    zed = [0] * arrsz
    arr = (c.c_int8 * arrsz)(*zed)
    return arr

def __multiply_matrices(list1, list2):
    buf = __malloc(2048)
    in1 = __pass_list_as_array(rows[0])
    in2 = __pass_list_as_array(rows[0])

    mtrx.coladd_different_matrices(buf, in1, in2, 2048, 2048)

    return __pass_array_as_list(buf)

def __run_model_step(rows: list):
    row0 = __multiply_matrices(rows[0], rows[0])
    row1 = __multiply_matrices(rows[1], rows[1])
    row2 = __multiply_matrices(rows[2], rows[2])
    row3 = __multiply_matrices(rows[3], rows[3])

    r1 = __multiply_matrices(row0, row2)
    r2 = __multiply_matrices(row1, row3)
    rf = __multiply_matrices(r1, r2)

    t0 = __multiply_matrices(rows[4], rows[6])
    t1 = __multiply_matrices(rows[5], rows[7])
    tf = __multiply_matrices(t0, t1)

    row0 = __multiply_matrices(row0, rows[4])
    row1 = __multiply_matrices(row1, rows[5])
    row2 = __multiply_matrices(row2, rows[6])
    row3 = __multiply_matrices(row3, rows[7])

    row0 = __multiply_matrices(row0, row2)
    row1 = __multiply_matrices(row1, row3)
    row0 = __multiply_matrices(row0, t0)
    row1 = __multiply_matrices(row1, t1)

    row0 = __multiply_matrices(row0, row1)
    row0 = __multiply_matrices(row0, tf)

    out = util.batch_arr2flt(row0)
    out.extend(util.batch_arr2flt(tf))
    out.extend(util.batch_arr2flt(rf))

    tns = torch.tensor(out)
    data = model_network(tns)

    return data.tolist()

def __rowclean(rows):
    if len(rows[0]) > 2048:
        del rows[0][0 : (len(rows[0]) - 2048)]
        del rows[1][0 : (len(rows[1]) - 2048)]
        del rows[2][0 : (len(rows[2]) - 2048)]
        del rows[3][0 : (len(rows[3]) - 2048)]
        del rows[4][0 : (len(rows[4]) - 2048)]
        del rows[5][0 : (len(rows[5]) - 2048)]
        del rows[6][0 : (len(rows[6]) - 2048)]
        del rows[7][0 : (len(rows[7]) - 2048)]
    elif len(rows[0]) < 2048:
        __pad(rows[0], 2048)
        __pad(rows[1], 2048)
        __pad(rows[2], 2048)
        __pad(rows[3], 2048)
        __pad(rows[4], 2048)
        __pad(rows[5], 2048)
        __pad(rows[6], 2048)
        __pad(rows[7], 2048)

    return rows

def __rows_push(rows, outdata):
    rows[0].append(util.flt2arr(outdata[0]))
    rows[1].append(util.flt2arr(outdata[1]))
    rows[2].append(util.flt2arr(outdata[2]))
    rows[3].append(util.flt2arr(outdata[3]))
    rows[4].append(util.flt2arr(outdata[4]))
    rows[5].append(util.flt2arr(outdata[5]))
    rows[6].append(util.flt2arr(outdata[6]))
    rows[7].append(util.flt2arr(outdata[7]))
    return rows

class LanguageModel(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.size = int(size * 3)
        self.flatten = nn.Flatten()

        halfsize = int(self.size / 2)
        thirdsize = int(self.size / 3)

        self.stack = nn.Sequential(nn.Linear(self.size, halfsize),
                                   nn.Tanhshrink(),
                                   nn.Linear(halfsize, thirdsize),
                                   nn.Tanh(),
                                   nn.Linear(thirdsize, thirdsize),
                                   nn.Tanhshrink(),
                                   nn.Linear(thirdsize, 1768),
                                   nn.Tanh(),
                                   nn.Linear(1768, 8),
                                   nn.Tanh())

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.stack(x)
        return logits

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
    mtrx.coladd_different_matrices.argtypes = c.POINTER(c.c_int8),c.POINTER(c.c_int8),c.POINTER(c.c_int8),c.c_uint64,c.c_uint64
    mtrx.coladd_different_matrices.restypes = None

    dprint("Creating model...")
    device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
    dprint(f"Using device {device}!")

    model_network = LanguageModel(2048).to(device)

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
        speaking_tokens = []

        encoded = tok.encode(inp, out_type='immutable_proto')
        for n in encoded.pieces:
            data = util.token_to_data(n.id, n.begin)
            # print(data)

            rows[0].append(data[0])
            rows[1].append(data[1])
            rows[2].append(data[2])
            rows[3].append(data[3])
            rows[4].append(data[4])
            rows[5].append(data[5])
            rows[6].append(data[6])
            rows[7].append(data[7])

        for i in range(256):
            rows = __rowclean(rows)

            outdata = __run_model_step(rows)
            speaking_tokens.append(util.fdata_to_token(outdata) % 4096)

            rows == __rows_push(rows, outdata)

        print(tok.decode(speaking_tokens))
else:
    sys.exit("This system does not support being run as an importable module at this time.")
