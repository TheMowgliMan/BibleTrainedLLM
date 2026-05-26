import math
import random

radius = 16

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def arr2flt(val: int) -> float:
    try:
        return float((abs(val) / val) * (2 ** (abs(val) / 16) - 1))
    except ZeroDivisionError:
        return float((2 ** (abs(val) / 16) - 1))

def flt2arr(val: float) -> int:
    try:
        return int((abs(val) / val) * math.trunc(clamp(math.log(abs(val) + 1, 2) * 16, -128, 127)))
    except ZeroDivisionError:
        return int(math.trunc(clamp(math.log(abs(val) + 1, 2) * 16, -128, 127)))

def batch_arr2flt(list_: list[float]):
    ret = []
    for item in list_:
        ret.append(arr2flt(item))
    return ret

def __negativize(n: int):
    if n > radius:
        return radius - n
    else:
        return n

def __denegativize(n: int):
    if n < radius:
        return -1 * n + radius
    else:
        return n

def token_to_data(tok_id: int, tok_start: int):
    ret = [0, 0, 0, 0, 0, 0, 0, 0]

    # Token encoding
    ret[0] = __negativize(tok_id % (2 * radius))
    ret[1] = __negativize(math.floor(tok_id / radius / 2) % (2 * radius))
    ret[2] = __negativize(math.floor(tok_id / (radius * 2) ** 2) % (2 * radius))

    # Positional encodings
    start_floats = (math.sin(tok_start), math.cos(tok_start), math.sin(tok_start / 2007 ** (0.5)), math.cos(tok_start / 2007 ** (0.5)))

    ret[4] = flt2arr(start_floats[0] * (16 / radius))
    ret[5] = flt2arr(start_floats[1] * (16 / radius))
    ret[6] = flt2arr(start_floats[2] * (16 / radius))
    ret[7] = flt2arr(start_floats[3] * (16 / radius))

    # Seeded random
    random.seed(tok_id)
    ret[3] = random.randint(-1 * radius, radius)

    return ret

def fdata_to_token(tok: list[float]):
    proc = []
    for item in tok:
        proc.append(flt2arr(item))

    return data_to_token(proc)

def data_to_token(tok: list[int]):
    ret = __denegativize(tok[0])
    ret += __denegativize(tok[1]) * radius * 2
    ret += __denegativize(tok[2]) * (radius * 2) ** 2
    return ret
