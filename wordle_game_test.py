#!/usr/bin/env python3

import unittest
from wordle_game import *

class WordleGameTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.game = WordleGame(['spam', 'eggs', 'span', 'pain', 'mess'], 'spam', 4, 2, False)

    def test_init(self):        
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(0, self.game.current_attempt)

    def test_word_too_long(self):
        with self.assertRaises(InvalidWordError):
            self.game.guess('spain')

    def test_word_not_existing(self):
        with self.assertRaises(InvalidWordError):
            self.game.guess('spal')

    def test_too_many_guesses(self):
        self.game.guess('pain')
        self.game.guess('pain')
        with self.assertRaises(OutOfGuessesError):
            self.game.guess('pain')

    def test_guess_correct(self):        
        result = self.game.guess('spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

    def test_guess_correct_is_case_insensitive(self):        
        result = self.game.guess('Spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

    def test_last_guess_successful(self):
        result = self.game.guess('pain')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨🟨⬜⬜', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

        result = self.game.guess('spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.hint)
        self.assertEqual(False, self.game.guesses_left())
        self.assertEqual(2, self.game.current_attempt)

    def test_one_letter_wrong(self):        
        result = self.game.guess('span')
        self.assertFalse(result.is_success)
        self.assertEqual('🟩🟩🟩⬜', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

    def test_two_letters_contained(self):        
        result = self.game.guess('Pain')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨🟨⬜⬜', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

    def test_strict_mode_chars_missing(self):
        strict_mode_game = WordleGame(['spam', 'mess', 'pain'], 'spam', 4, 2, True)
        strict_mode_game.guess('mess')
        with self.assertRaises(InvalidInStrictModeError):
            strict_mode_game.guess('pain')

    # Implementation detail of original Wordle: When a letter has more occurrences in the guess
    # than in the solution, the number of 🟨 is only equal (or lower) than the number of 
    # occurences in the solution. It can be lower when there are direct matches (🟩)
    def test_yellow_hint(self):
        
        self.assert_hint('spam', 'mess', '🟨⬜🟨⬜',  
            '"s" occurs only once in the solution, so only one 🟨 is displayed for the "s"')
        
        self.assert_hint('harass', 'tossed', '⬜⬜🟨🟨⬜⬜',          
            '"s" occurs twice in the solution, so two 🟨 are displayed')

        self.assert_hint('tossed', 'schuss', '🟨⬜⬜⬜🟨⬜',          
            '"s" occurs only twice in the solution, so only two 🟨 are displayed')

        self.assert_hint('post', 'mess', '⬜⬜🟩⬜',          
            '"s" occurs only once in the solution and the only occurence is a direct match')

        self.assert_hint('chill', 'lulls', '🟨⬜⬜🟩⬜',          
            'Second "l" is not displayed as 🟨 because the third one is a direct match')

        self.assert_hint('xyxxy', 'xxxxz', '🟩⬜🟩🟩⬜',          
            '"x" occurs only three times in the solution, and all occurences are direct matches')
        
    def assert_hint(self, solution, guess, expected_hint, message):
        special_game = WordleGame([solution, guess], solution, len(solution), 1, False)
        self.assertEqual(expected_hint, special_game.guess(guess).hint, message)

unittest.main()

