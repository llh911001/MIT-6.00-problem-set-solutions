# Problem Set 6 #1,#2 (initially a copy of Problem Set 5: 6.00 Word Game)
# Name: 
# Collaborators: 
# Time: 
#

import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    ##print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    ##print "  ", len(wordlist), "words loaded."
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

#
# Problem #1: Scoring a word
#
def get_word_score(word, n=HAND_SIZE):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = 0
    if word:
        for letter in word:
            score += SCRABBLE_LETTER_VALUES[letter]
        if len(word) == n:
            score += 50
    return score



#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,              # print all on the same line
    print                              # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = {}
    word_freq = get_frequency_dict(word)
    for letter in hand:
        new_hand[letter] = hand[letter] - word_freq.get(letter, 0)
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    word_dict = get_frequency_dict(word) # convert string to dictionary(string -> int), same as hand
    for key in word_dict:
        if word_dict[key] > hand.get(key, 0):
            return False
    return word in word_list

#
# Problem #4: Playing a hand (of pset 5)
# Problem #1, #2 (of pset 6)
#
def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    total_score = 0
    time_limit = input("Enter time limit, in seconds, for players: ")
    time_left = time_limit
    assert isinstance(time_limit, int) and time_limit > 0, "Not an integer, or less than 0."
    while True:
        print "Current hand:",
        display_hand(hand)
        start_time = time.time()
        entered = raw_input("Enter word, or a . to indicate that you are finished: ")
        end_time = time.time()
        time_took = end_time - start_time # time spent while enter word
        time_left -= time_took
        word = entered.strip()

        if time_left >= 0:
            if word == '.':
                break
            if not is_valid_word(word, hand, points_dict):
                print "Invalid word input: not a word. please try again.\n"
                continue

            print "It took %.2f seconds to provide an answer." % time_took

            # after a little experiment, which is, let Python excute the following code:
            # >>>start = time.time();end = time.time();print end-start
            # I found that the result on my laptop is around 1e-6(it may vary on other computers), so I suppose a human can not input a word in less
            # than 1e-6 senconds(he has to spend some time to think), and 1e-6 certainly can divide an integer without throw a zero divide error.
            # So I just let time took divide the score.
            score = get_word_score(word)/time_took
            total_score += score
            print "%r earned %d Points. Total: %d\n" % (word, score, total_score)
            hand = update_hand(hand, word)
        else:
            print "Total time exceeds %d seconds. You scored %.2f points" % (time_limit, total_score)
            break
    # on exit
    print "Total score: %.2f points." % total_score

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO ...
#    print "play_game not implemented."         # delete this once you've completed Problem #4
#    play_hand(deal_hand(HAND_SIZE), word_list) # delete this once you've completed Problem #4

    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'r':
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'e':
            break
        else:
            print "Invalid command."

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    #play_game(word_list)
    play_hand(dict(a=1,c=1,i=1,h=1,m=2,z=1), word_list)

