import argparse
import sys
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', type=str, choices=['seq', 'perm'])
    parser.add_argument('-n', '--num-keys', type=int)
    return parser.parse_args()

def main():
    args = parse_args()
    if (args.pattern == 'seq'):
        keys = range(args.num_keys)
    elif (args.pattern == 'perm'):
        keys = np.random.permutation(args.num_keys)
    print(' '.join(map(lambda x: str(x), keys)))

if __name__ == '__main__':
    main()
