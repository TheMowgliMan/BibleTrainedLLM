import math

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def arr2flt(val: int) -> float:
    try:
        return float((abs(val) / val) * (2 ** (abs(val) / 32) - 1))
    except ZeroDivisionError:
        return float((2 ** (abs(val) / 32) - 1))

def flt2arr(val: float) -> int:
    try:
        return int((abs(val) / val) * math.trunc(clamp(math.log(abs(val) + 1, 2) * 32, -128, 127)))
    except ZeroDivisionError:
        return int(math.trunc(clamp(math.log(abs(val) + 1, 2) * 32, -128, 127)))
