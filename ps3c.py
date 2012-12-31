#!/usr/bin/env python

# Problem 3.

from string import *
from ps3b import subStringMatchExact

#  target strings

target1 = 'atgacatgcacaagtatgcat'
target2 = 'atgaatgcatggatgtaaatgcag'

# key strings

key10 = 'a'
key11 = 'atg'
key12 = 'atgc'
key13 = 'atgca'


def constrainedMatchPair(firstMatch, secondMatch, length):
    """ return a tuple of all members (call it n) of the first tuple for which there is an element in the second tuple (call it k) such that n+m+1 = k, where m is the length of the first substring. """
    contranined_match_pair = ()
    for n in firstMatch:
        for k in secondMatch:
            if n + length + 1 == k:
                contranined_match_pair += (n,)
    return contranined_match_pair


def subStringMatchOneSub(key,target):
    """search for all locations of key in target, with one substitution"""
    allAnswers = ()
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        ### print 'breaking key "%s" into "%s", "%s"' % (key, key1, key2)
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
        ### print 'match1:', match1
        ### print 'match2:', match2
        ### print 'possible matches for "%s", "%s" start at:' % (key1, key2), filtered
    return allAnswers

def test(targets, keys):
    for t in targets:
        for k in keys:
            print "target: %s\nkey: %s" % (t, k)
            print subStringMatchOneSub(k, t)
            print '-'*100


if __name__ == '__main__':
    test([target1, target2], [key10, key11, key12, key13])
