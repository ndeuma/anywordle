#!/usr/bin/env python3

# Try to find a set of words that contains the maximum number of different letters
#
# In English, it is possible to use 25 letters with 5 5-letter words (some of them are very unusual)
# BRICK, GLENT, JUMPY, VOZHD, WAQFS
# These are valid inputs in the original Wordle.
# See also: https://www.reddit.com/r/wordle/comments/s0qjrj/five_words_that_use_25_different_letters/hvh4iup

# The best combination I found so far in German is:
# ENZYM, GICHT, LUXUS, BIWAK, FJORD (23 letters)
# (not considerung words with Ä, Ö, Ü, ß)
# These are valid inputs on https://wordle.at/
#
# However, this program hasn't been run on a full wordlist yet - takes too long and needs further optimization.

import argparse
from functools import reduce
import re

DEFAULT_WORDLIST_EN_US = '/usr/share/dict/american-english'
DEFAULT_WORDLIST_EN_UK = '/usr/share/dict/british-english'

def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='Try to find a set of words that contains the maximum number of letters', 
        argument_default=argparse.SUPPRESS)
    parser.add_argument('wordlist', nargs='?', default='',
        help='Word list file (default: English \'dict\' dictionary files)')
    parser.add_argument('-n', '--nwords', default=5,
        help='Number of words to find (default: 5)')    
    parser.add_argument('-l', '--length', default=5,
        help='Length of each word to (default: 5)')        
    return parser

def normalize(args, words):
    letters_only = re.compile('^[a-z]{' + str(args.length) + '}$')
    return list(set( 
        filter(lambda w: len(w) == int(args.length) and letters_only.match(w), 
        map(lambda s: s[0:-1].lower(), words)))) # Remove trailing newline

def read_and_normalize(args, *word_list_files):
    words = []
    for word_list_file in word_list_files:        
        with open(word_list_file) as file:
            words = words + file.readlines()
    return normalize(args, words)

def get_contained_letters(word_set):
    return reduce(lambda s1, s2: set(s1).union((set(s2))), word_set)

# 1. Pick one word
# 2. Add the letters of this word to the set of "forbidden" letters
# 3. Filter the remaining list of words, so that only words that contain no "forbidden" letters remain
# 4. Call yourself recursively with the set of forbidden letters, the new list of words and one
#    word less to find.
# 5. If this does not find a better set, try steps 3 and 4 with a list of words that can contain one 
#    "forbidden" letter.
def max_letters_word_set(candidate_words, nwords, forbidden_letters):        
    if (len(candidate_words) == 0 or nwords == 0):
        return set()

    max_set = set()
    max = 0
    for candidate in candidate_words:                        
        new_forbidden_letters = forbidden_letters.union(set(candidate))
        for intersect_size in range(0, 2):
            new_words = list(filter(lambda w: len(set(w).intersection(new_forbidden_letters)) == intersect_size, 
                candidate_words))        
            word_set = max_letters_word_set(new_words, nwords - 1, new_forbidden_letters)            
            new_set = word_set.union({candidate})            
            n_letters = len(get_contained_letters(new_set))
            if n_letters > max: 
                max = n_letters
                max_set = new_set
            # No need to try intersection size 1 when the recursive call with intersection size 0 found something
            if len(word_set) > 0:
                break
    return max_set
      

args = create_arg_parser().parse_args()

if args.wordlist == '':
    words = read_and_normalize(args, DEFAULT_WORDLIST_EN_UK, DEFAULT_WORDLIST_EN_US)
else:
    words = read_and_normalize(args, args.wordlist)

max_letter_count = 0

max_set = max_letters_word_set(words, int(args.nwords), set())
print(f"max_set = {max_set}, contained_letters = {len(get_contained_letters(max_set))}")        




