#!/usr/bin/env python3

import argparse
import random
import re
from wordle_game import *

DEFAULT_WORDLIST_EN_US = '/usr/share/dict/american-english'
DEFAULT_WORDLIST_EN_UK = '/usr/share/dict/british-english'

def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='A highly configurable implementation of the \'Wordle\' word-guessing game.', 
        argument_default=argparse.SUPPRESS)
    parser.add_argument('wordlist', nargs='?', default='',
        help='Word list file (default: English \'dict\' dictionary files)')
    parser.add_argument('-a', '--attempts', default=6,
        help='Allowed number of attempts (default: 6)')    
    parser.add_argument('-l', '--length', default=5,
        help='Length of word to guess (default: 5)')    
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
        help='Print detailed output')
    return parser

def normalize(args, words):
    letters_only = re.compile('^[a-z]{' + str(args.length) + '}$')
    return list(set( 
        filter(lambda w: len(w) == int(args.length) and letters_only.match(w), 
        map(lambda s: s[0:-1].lower(), words)))) # Remove trailing newline

def read_and_normalize(args, *word_list_files):
    words = []
    for word_list_file in word_list_files:
        if args.verbose:
            print(f'Adding word list file: {word_list_file}')
        with open(word_list_file) as file:
            words = words + file.readlines()
    return normalize(args, words)

args = create_arg_parser().parse_args()

if args.wordlist == '':
    words = read_and_normalize(args, DEFAULT_WORDLIST_EN_UK, DEFAULT_WORDLIST_EN_US)
else:
    words = read_and_normalize(args, args.wordlist)

if (args.verbose):
    print(f'Read {len(words)} words')

solution = words[random.randint(0, len(words) - 1)]

game = WordleGame(words, solution, int(args.length), int(args.attempts), False)

while game.guesses_left():
    try:
        result = game.guess(input(f'Attempt {game.current_attempt + 1}/{game.attempts}: '))
        if (result.is_success):
            print('Congratulations!')
            break
        elif not game.guesses_left():
            print(f'The word is: {game.solution}')
        else:
            print(result.hint)
    except InvalidWordError as err:
        print(err)

    







