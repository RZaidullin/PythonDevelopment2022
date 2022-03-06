from . import *
import sys
import urllib.request


if __name__ == "__main__":
    dictionary = sys.argv[1]
    length = 5 if len(sys.argv) < 3 else int(sys.argv[2])
    try:
        with open(dictionary, 'r') as f:
            words = f.read().split()
    except Exception:
        words = urllib.request.urlopen(dictionary).read().decode().split()
    valid_words = [i for i in words if len(i) == length]
    print(gameplay(ask, inform, valid_words))
