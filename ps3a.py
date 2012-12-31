#!/usr/bin/env python

#####################################
# Problem 1.
# Write two functions, called countSubStringMatch and countSubStringMatchRecursive that
# take two arguments, a key string and a target string. These functions iteratively and recursively count
# the number of instances of the key in the target string. You should complete definitions for
# def countSubStringMatch(target,key):
# and
# def countSubStringMatchRecursive(target, key):
# Place your answer in a file named ps3a.py
#####################################

from string import *

def countSubStringMatch(target, key):
    """ count matched instances iteratively """
    count = 0
    start_index = 0
    while start_index < len(target):
        match_index = find(target, key, start_index)
        if match_index != -1:
            count += 1
            start_index = match_index + (len(key) or 1) # if key is a blank string, we start finding from next element of the target.
        else:
            start_index += 1
    return count

def countSubStringMatchRecursive(target, key):
    """ count matched instances recursively """
    match_index = find(target, key)
    if match_index == -1:
        return 0
    else:
        target = target[match_index+(len(key) or 1):]
        return 1 + CountSubStringMatchRecursive(target, key)

