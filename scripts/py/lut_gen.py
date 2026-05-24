import math
from util import *

# Array values can be converted to floats with the following function: Given n, m = float((abs(n) / n) * 2 ** (abs(n) / 32) - 1)
# Vice-verse: Given m, n = math.trunc(clamp(math.log(n + 1, 2) * 32, -128, 127))

if __name__ == "__main__":
    with open("lut.h", "w") as lut:
        lut.write("#include <stdint.h>\n")
        # Don't need mult/div tables due to the math involved
        # Add/sub tables
        lut.write("int8_t add_tbl[65536] = {\n")
        for x in range(-128, 128, 1):
            for y in range(-128, 128, 1):
                val = flt2arr(arr2flt(x) + arr2flt(y))
                lut.write(str(val))
                lut.write(",\n")
        lut.write("};\n")
