import argparse
import sys
import numpy as np


def gen_seq(args):
    return range(args.num_keys)

def gen_perm(args):
    return np.random.permutation(args.num_keys)

def gen_uni(args):
    assert(args.max_key % 100 == 0)
    assert(0 < args.percent <= 100)
    def sample():
        return (100 * np.random.randint(args.max_key // 100)
                + np.random.randint(args.percent))
    return [sample() for _ in range(args.num_keys)]

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='key pattern')

    parser_seq = subparsers.add_parser('seq', help='sequential pattern')
    parser_seq.add_argument('-n', '--num-keys', type=int, required=True)
    parser_seq.set_defaults(generate=gen_seq)

    parser_perm = subparsers.add_parser('perm', help='permutation pattern')
    parser_perm.add_argument('-n', '--num-keys', type=int, required=True)
    parser_perm.set_defaults(generate=gen_perm)

    parser_uni = subparsers.add_parser('uni', help='uniform pattern')
    parser_uni.add_argument('-n', '--num-keys', type=int, required=True)
    parser_uni.add_argument('-m', '--max-key', type=int, required=True)
    parser_uni.add_argument('-p', '--percent', type=int, required=True)
    parser_uni.set_defaults(generate=gen_uni)

    return parser.parse_args()

def main():
    args = parse_args()

    keys = args.generate(args)

    print(' '.join(map(lambda x: str(x), keys)))

if __name__ == '__main__':
    main()
