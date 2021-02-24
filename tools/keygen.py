#!/usr/bin/env python3

import argparse
import sys
import numpy as np
import multiprocessing as mp
from itertools import chain


def gen_seq(args):
    return range(args.num_keys)

def gen_perm(args):
    return np.random.permutation(args.num_keys)

def gen_uni_task(args):
    chunk_size = args.num_keys // mp.cpu_count()
    return [(100 * np.random.randint(args.max_key // 100)
             + np.random.randint(args.percent))
            for _ in range(chunk_size)]

def gen_uni(args):
    assert(args.max_key % 100 == 0)
    assert(0 < args.percent <= 100)
    assert(args.num_keys % mp.cpu_count() == 0)

    with mp.Pool(mp.cpu_count()) as pool:
        keys_list = pool.map(gen_uni_task, [args for _ in range(mp.cpu_count())])

    return list(chain(*keys_list))

def gen_zipf(args):
    class ZipfGenerator:
        # https://stackoverflow.com/questions/31027739/python-custom-zipf-number-generator-performing-poorly
        def __init__(self, n, alpha):
            tmp = np.power(np.arange(1, n+1) , -alpha)
            zeta = np.r_[0, np.cumsum(tmp)]
            self.dist_map = np.array([x / zeta[-1] for x in zeta])

        def next(self, n=1):
            u = np.random.random(n)
            return np.searchsorted(self.dist_map, u) - 1

    zgen = ZipfGenerator(args.max_key, args.skew)
    return zgen.next(args.num_keys)

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

    parser_zipf = subparsers.add_parser('zipf', help='zipfian pattern')
    parser_zipf.add_argument('-n', '--num-keys', type=int, required=True)
    parser_zipf.add_argument('-m', '--max-key', type=int, required=True)
    parser_zipf.add_argument('-s', '--skew', type=float, required=True)
    parser_zipf.set_defaults(generate=gen_zipf)

    return parser.parse_args()

def main():
    args = parse_args()

    keys = args.generate(args)

    print(' '.join(map(lambda x: str(x), keys)))

if __name__ == '__main__':
    main()
