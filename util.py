import math
import random

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

def token_to_data(tok_id: int, tok_start: int, radius=16):
    ret = [0, 0, 0, 0, 0, 0, 0, 0]

    # Token encoding
    ret[0] = tok_id % (2 * radius) - radius
    ret[1] = math.floor(tok_id / radius / 2) % (2 * radius) - radius
    ret[2] = math.floor(tok_id / (radius * 2) ** 2) % (2 * radius) - radius

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

def data_to_token(tok: list[int], radius=16):
    ret = tok[0] + radius
    ret += (tok[1] + radius) * radius * 2
    ret += (tok[2] + radius) * (radius * 2) ** 2
    return ret
