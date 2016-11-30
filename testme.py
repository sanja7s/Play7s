#!/usr/bin/env python
# better.py
import sys
import numpy as np



def reservoir_sampling(k, sample, data):
    """
        uses probability calculation that after k, 
        each new element should be added with
        probability 1/k to the sample and in that case a
        random one from the current elements should be removed 
    """

    i = 0
    while len(sample) < k and i < len(data):
        el = data[i]
        i += 1
        sample.append(el)

    if len(sample) == k:
        for j in range(i, len(data)):
            el = data[j] 
            if np.random.random() < 1.0/k:
                rnd_index = np.random.randint(0,k)
                sample[rnd_index] = el

def print_sample(sample):
    for el in sample:
        el = el.encode('utf-8')
        sys.stdout.write(el)
    print

BUFFER_SIZE=4096

def read_from_stdin_text(fn, k, sample, buffer_size=BUFFER_SIZE):
    while True:
        buf = sys.stdin.readline(buffer_size)
        if not buf:
            break
        fn(k, buf, sample)

def read_from_stdin_binary(fn, k, sample, buffer_size=BUFFER_SIZE):
    while True:
        buf = sys.stdin.read(buffer_size)
        if buf == None:
            continue
        if not buf:
            break
        fn(k, buf, sample)

# fn is a lambda buf: ...., buf is either a string or byte array
def read_from_stdin(fn, k, sample, buffer_size=BUFFER_SIZE):
    if sys.stdin.isatty():
        read_from_stdin_text(fn, k, sample, buffer_size)
    else:
        read_from_stdin_binary(fn, k, sample, buffer_size)



k = 6
sample = []

read_from_stdin(lambda k, data, sample: reservoir_sampling(k, sample, data), k, sample)
print 'SAMPLE SIZE ', k
print_sample(sample)