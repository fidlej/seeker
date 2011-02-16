#!/usr/bin/env python
"""Usage: seeker.py /path/to/raw/device
Measures the possible number of seeks per seconds.
"""

import os
import sys
import time
import random

BLOCKSIZE = 512

def _get_size(input):
    input.seek(0, os.SEEK_END)
    return input.tell()


def _seek_randomly(dev, size, num_seeks):
    num_blocks = size // BLOCKSIZE
    for i in xrange(num_seeks):
        block = random.randrange(num_blocks)
        dev.seek(block * BLOCKSIZE)
        dev.read(BLOCKSIZE)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    dev = open(filename)
    size = _get_size(dev)
    print "Benchmarking %s [%s MB]" % (filename, size//2**20)

    random.seed()
    num_seeks = 10000
    start = time.time()
    _seek_randomly(dev, size, num_seeks)
    end = time.time()

    duration = end - start
    print "%s/%s = %s seeks/second" % (
            num_seeks, duration, int(num_seeks/float(duration)))
    print "%.2f ms random access time" % (1000 * duration/float(num_seeks))


if __name__ == "__main__":
    main()
