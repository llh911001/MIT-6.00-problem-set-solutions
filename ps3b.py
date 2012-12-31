#!/usr/bin/env python

# Problem 2.

from string import *

def subStringMatchExact(target, key):
    """ return a tuple of the starting index of all matched sub strings. """
    matches = ()
    start_index = 0
    while start_index < len(target):
        match_index = find(target, key, start_index)
        if match_index != -1:
            matches += (match_index,)
            start_index = match_index + (len(key) or 1)
        else:
            start_index += 1
    return matches
