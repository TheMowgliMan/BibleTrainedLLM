import sys
import argparse

try:
    import sentencepiece as spm
except ModuleNotFoundError:
    sys.exit("This cannot be built without SentencePiece installed!\nTry running 'pip3 install sentencepiece'")

try:
    from transformers import DebertaV2Tokenizer
except ModuleNotFoundError:
    sys.exit("This cannot be built without Transformers installed!\nTry running 'pip3 install transformers'")

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("data")
    parsed = parse.parse_args()

    spm.SentencePieceTrainer.Train(input=parsed.data,
                                   model_prefix="homebrewModel",
                                   vocab_size=4096,
                                   pad_id=0,
                                   unk_id=1,
                                   bos_id=2,
                                   eos_id=3,
                                   pad_piece="~{{PAD}}~",
                                   unk_piece="~{{UNK}}~",
                                   bos_piece="~{{BOS}}~",
                                   eos_piece="~{{EOS}}~",
                                   model_type='unigram')

    # sp = spm.SentencePieceProcessor(model_file='homebrewModel.model')
    # encoded = sp.encode(['This is a test, of many different things. COMPUTER buh heHE Do I not have uppercase letter U/u lol', 'Hello world'], out_type='immutable_proto')
    # print(encoded)
