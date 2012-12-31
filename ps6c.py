# Problem Set 6 #4 (initially a copy of Problem Set 6 #1,#2)
# Name: 
# Collaborators: 
# Time: 
#

import random
import string
import time
import itertools


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


def get_words_to_points(word_list):
    """
    return a dict where the keys are words in word_list and values are the correponding word's points.
    """
    points_dict = {}
    for word in word_list:
        points_dict[word] = get_word_score(word)
    return points_dict


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
    for letter in word:
        hand[letter] -= 1
    return dict((k, v) for k, v in hand.items() if v > 0)

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, points_dict):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    points_dict: dictionary of word and points as key and value
    """
    letter_freq = get_frequency_dict(word) # convert string to dictionary(string -> int), same as hand
    for key in letter_freq:
        if letter_freq[key] > hand.get(key, 0):
            return False
    return word in points_dict # Time complexity is O(1)


#
# Problem #4: Playing a hand
#

# problem #3 of pset 6
def get_time_limit(points_dict, k=1):
    """
    Return the time limit for the computer player as a function of the
    multiplier k.
    points_dict should be the same dictionary that is created by
    get_words_to_points.
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.

    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word)
        end_time = time.time()
    return (end_time - start_time) * k


# problem #4 of pset 6
def get_hand_subsets(hand):
    """
    hand_subsets is subsets of the letters of hand.
    """
    letters = [c for c in hand for i in range(hand[c])]
    hand_subsets = ()
    for i in range(1, len(letters)+1):
        for tup in set(itertools.combinations(letters, i)):
            hand_subsets += (''.join(sorted(tup)), )
    return hand_subsets


# problem #4 of pet 6
def get_word_rearrangement(word_list):
    """
    return a dict which the keys are string containing the letters of word in sorted order,
    and the values are the word.
    """
    rearrange_dict = {}
    for word in word_list:
        sorted_word_string = ''.join(sorted(word))
        rearrange_dict[sorted_word_string] = word
    return rearrange_dict

# problem #4 of pset 6
def pick_best_word_faster(hand, rearrange_dict):
    """
    much faster than pick_best_word in problem #3.
    """
    hand_subsets = get_hand_subsets(hand)
    valid_words = []
    for subset in hand_subsets:
        sorted_subset_string = ''.join(sorted(subset))
        if sorted_subset_string in rearrange_dict:
            valid_words.append(rearrange_dict[sorted_subset_string])
    if valid_words:
        words_points = [(word, get_word_score(word)) for word in valid_words]
        best_word = max(words_points, key=lambda x: x[1])[0]
        return best_word
    print "%r can not make any word, hand over.\n" % ''.join(c for c in hand for i in range(hand[c]))
    return '.'

def play_hand(hand, points_dict, rearrange_dict, time_limit): # problem #4 of pset 6
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
    time_left = time_limit
    while True:
        print "Current hand:",
        display_hand(hand)
        start_time = time.time()
        #entered = raw_input("Enter word, or a . to indicate that you are finished: ")
        #word = entered.strip()
        word = pick_best_word_faster(hand, rearrange_dict) # problem #4 of pset 6
        end_time = time.time()
        time_took = end_time - start_time # time spent while enter word
        time_left -= time_took

        if time_left >= 0:
            if word == '.':
                break
            if not is_valid_word(word, hand, points_dict):
                print "Invalid word input: not a word. please try again.\n"
                continue

            print "It took %.4f seconds to provide an answer." % time_took
            print "Computer chose %r." % word
            score = get_word_score(word)/time_took
            total_score += score
            print "%r earned %.2f Points. Total: %.2f\n" % (word, score, total_score)
            hand = update_hand(hand, word)
        else:
            print "Total time exceeds %.4f seconds. Computer scored %.2f points." % (time_limit, total_score)
            break
    # on exit
    print "Total score: %.2f Points." % total_score

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(points_dict, rearrange_dict, time_limit):
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
#    play_hand(deal_hand(HAND_SIZE), points_dict) # delete this once you've completed Problem #4

    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), points_dict, rearrange_dict, time_limit)
            print
        elif cmd == 'r':
            play_hand(hand.copy(), points_dict, rearrange_dict, time_limit)
            print
        elif cmd == 'e':
            break
        else:
            print "Invalid command."

### for fun ###
def is_palindrome(word):
    if len(word) <= 1:
        return True
    elif word[0] == word[-1]:
        return is_palindrome(word[1:-1])
    return False
# is_palindrome = lambda w: w[:] == w[::-1]

def palindrome(word_list):
    res = []
    for word in word_list:
        if is_palindrome(word):
            res.append(word)
    return res

# palindrome = filter(lambda w: w[:] == w[::-1], word_list)
### end for fun ###

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    points_dict = get_words_to_points(word_list)
    time_limit = get_time_limit(points_dict, k=1)
    rearrange_dict = get_word_rearrangement(word_list)
    print "Time limit: ", time_limit
    #play_game(points_dict, rearrange_dict, time_limit)
    play_hand(get_frequency_dict('pointsn'), points_dict, rearrange_dict, time_limit)
