# Problem Set 5: Ghost
# Name: 
# Collaborators: 
# Time: 
#

import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

def is_begin_of_word(fragment):
    """Check if there are words begin with the fragment, and the fragment itself is not a word."""
    for word in wordlist:
        if word.startswith(fragment) and fragment != word:
            return True
    return False

def ghost():
    """main game function"""
    fragment = ''
    players = [1, 2]
    print "Welcome to Ghost!\nPlayer 1 goes first."
    while True:
        for player in players:
            print "Current word fragment: %r" % fragment
            print "Player %d's turn." % player
            entered = raw_input("Player %d says letter: " % player)
            print
            letter = entered.strip().lower()
            if not letter or letter not in string.ascii_lowercase:
                print "Invalid letter input: should be one and only one letter(case insensitive). please try again."
                print
                if player == 2:
                    players = [2, 1]
                break
            fragment += letter
            if len(fragment) > 3 and fragment in wordlist:
                print "Current word fragment: %r\nPlayer %d loses because %r is a word!" % (fragment, player, fragment)
                players.remove(player)
                print "Player %d wins!" % players[0]
                return
            elif not is_begin_of_word(fragment):
                print "Current word fragment: %r\nPlayer %d loses because no word begins with %r!" % (fragment, player, fragment)
                players.remove(player)
                print "Player %d wins!" % players[0]
                return


if __name__ == '__main__':
    ghost()
