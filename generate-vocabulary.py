import sys
import argparse

try:
    import sentencepiece as spm
except ModuleNotFoundError:
    sys.exit("This cannot be built without SentencePiece installed!\nTry running 'pip3 install sentencepiece'")

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("data")
    parsed = parse.parse_args()

    with open(str(parsed.data)) as tok_train_data:
        td = tok_train_data.read()
