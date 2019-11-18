import sys
import numpy as np


def main():
    if len(sys.argv) != 2:
        print("Please provide the number of keys")
        print("ex) %s (#_of_key)" % sys.argv[0])
        sys.exit(1)

    count = int(sys.argv[1])
    keys = np.random.permutation(count)
    print(' '.join(map(lambda x: str(x), keys)))

if __name__ == '__main__':
    main()
