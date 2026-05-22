import sys

# We use error guards for silly people who run this without pytorch
try:
    import torch
    from torch import nn
except ModuleNotFoundError:
    sys.exit("This cannot be run without PyTorch installed!\nTry running 'pip3 install torch'")

import util

if __name__ == "__main__":
    pass
else:
    sys.exit("This system does not support being run as a module at this time.")
