#!/usr/bin/env python

def largest():
    n_list = range(1, 50)
    for n in n_list:
        for c in range(10):
            for b in range(10):
                for a in range(10):
                    if 6*a + 9*b + 20*c == n:
                        # if n McNuggets can be bought, change n to 0 in the list.
                        # the index of n is n-1.
                        n_list[n-1] = 0
    # sieve 0s out of the list, left ns are the number of McNs can't be bought.
    ret = [i for i in n_list if i]
    print 'Largest number of McNuggets that cannot be bought in exact quantity: %d' % ret[-1]


def is_solvable(n):
    #a, b, c = 0, 0, 0
    for a in range(10):
        #if 6*a + 9*b + 20*c == n:
        #    return 1
        for b in range(10):
            #if 6*a + 9*b + 20*c == n:
            #    return 1
            for c in range(10):
                if 6*a + 9*b + 20*c == n:
                    return 1
    return 0
