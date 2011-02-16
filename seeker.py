#!/usr/bin/env python
"""Usage: seeker.py /path/to/raw/device
Measures the possible number of seeks per seconds.
"""
# It should work on any Unix.
# It is based on the Linux specific seeker.c from:
# http://www.linuxinsight.com/how_fast_is_your_disk.html

import os
import sys
import time
import random

BLOCKSIZE = 512

def _get_size(input):
    input.seek(0, os.SEEK_END)
    size = input.tell()
    if size != 0:
        return size

    # FreeBSD does not support SEEK_END on devices.
    # We need to get the size by binary halving.
    pos = 0
    step = 2**40  # 1TB
    while True:
        pos += step
        try:
            input.seek(pos)
            data = input.read(1)
        except IOError, possible:
            data = ""

        if len(data) != 1:
            if step == 1:
                # Size is the possible position + 1.
                return (pos - step) + 1

            pos -= step
            step = max(1, step // 2)


def _seek_randomly(dev, size, num_seeks):
    num_blocks = size // BLOCKSIZE
    for i in xrange(num_seeks):
        block = random.randrange(num_blocks)
        dev.seek(block * BLOCKSIZE)
        data = dev.read(BLOCKSIZE)
        assert len(data) == BLOCKSIZE


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
