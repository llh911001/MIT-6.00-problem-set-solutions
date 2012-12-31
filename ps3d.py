#!/usr/bin/env python

# Problem 4.

from ps3b import subStringMatchExact
from ps3c import subStringMatchOneSub

#  target strings

target1 = 'atgacatgcacaagtatgcat'
target2 = 'atgaatgcatggatgtaaatgcag'

# key strings

key10 = 'a'
key11 = 'atg'
key12 = 'atgc'
key13 = 'atgca'


def subStringMatchExactlyOneSub(target, key):
    """ return a tuple of all starting points of matches of the key to the target, such that at exactly one element of the key is incorrectly matched to the target. """
    substring_match_exact = subStringMatchExact(target, key)
    substring_match_one_sub = subStringMatchOneSub(key, target)
    substring_match_exactly_one_sub = ()
    print substring_match_exact
    print substring_match_one_sub
    for index in substring_match_one_sub:
        if index not in substring_match_exact:
            substring_match_exactly_one_sub += (index,)
    return substring_match_exactly_one_sub

def test(targets, keys):
    for t in targets:
        for k in keys:
            print "target: %s\nkey: %s" % (t, k)
            print subStringMatchExactlyOneSub(t, k)

if __name__ == '__main__':
    test([target1, target2], [key10, key11, key12, key13])
