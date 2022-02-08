#!/usr/bin/env python3

import unittest
from wordle_game import *

class WordleGameTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.game = WordleGame(['spam', 'eggs', 'span', 'pain', 'mess'], 'spam', 4, 2, False)

    def test_init(self):        
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(0, self.game.attempts_made)

    def test_word_too_long(self):
        with self.assertRaises(InvalidWordError):
            self.game.guess('spain')        
        with self.assertRaises(InvalidWordError):
            self.game.guess('spine')
        self.assertEqual(0, self.game.attempts_made)

    def test_word_not_existing(self):
        with self.assertRaises(InvalidWordError):
            self.game.guess('spal')
        with self.assertRaises(InvalidWordError):
            self.game.guess('spuz')
        with self.assertRaises(InvalidWordError):
            self.game.guess('spoi')
        self.assertEqual(0, self.game.attempts_made)

    def test_too_many_guesses(self):
        self.game.guess('pain')
        self.game.guess('pain')
        with self.assertRaises(OutOfGuessesError):
            self.game.guess('pain')

    def test_guess_correct(self):        
        result = self.game.guess('spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.to_emoji())
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.attempts_made)

    def test_guess_correct_is_case_insensitive(self):        
        result = self.game.guess('Spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.to_emoji())
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.attempts_made)

    def test_last_guess_successful(self):
        result = self.game.guess('pain')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨🟨⬜⬜', result.to_emoji())
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.attempts_made)

        result = self.game.guess('spam')
        self.assertTrue(result.is_success)
        self.assertEqual('🟩🟩🟩🟩', result.to_emoji())
        self.assertEqual(False, self.game.guesses_left())
        self.assertEqual(2, self.game.attempts_made)

    def test_one_letter_wrong(self):        
        result = self.game.guess('span')
        self.assertFalse(result.is_success)
        self.assertEqual('🟩🟩🟩⬜', result.to_emoji())
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.attempts_made)

    def test_two_letters_contained(self):        
        result = self.game.guess('Pain')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨🟨⬜⬜', result.to_emoji())
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.attempts_made)

    def test_strict_mode_chars_missing(self):
        strict_mode_game = WordleGame(['spam', 'mess', 'pain'], 'spam', 4, 2, True)
        strict_mode_game.guess('mess')
        with self.assertRaisesRegex(InvalidInStrictModeError, 'The following letters must be contained in the guess: m, s'):
            strict_mode_game.guess('pain')
        self.assertEqual(1, strict_mode_game.attempts_made)

    def test_strict_mode_no_exact_match(self):
        strict_mode_game = WordleGame(['spam', 'spin', 'pain', 'sins'], 'spam', 4, 2, True)
        strict_mode_game.guess('spin')        
        with self.assertRaisesRegex(InvalidInStrictModeError, 'The letter at position 1 must be s'):
            strict_mode_game.guess('pain')
        with self.assertRaisesRegex(InvalidInStrictModeError, 'The letter at position 2 must be p'):
            strict_mode_game.guess('sins')
        self.assertEqual(1, strict_mode_game.attempts_made)

    # Implementation detail of original Wordle: When a letter has more occurrences in the guess
    # than in the solution, the number of 🟨 is only equal (or lower) than the number of 
    # occurences in the solution. It can be lower when there are direct matches (🟩)
    def test_yellow_hint(self):
        
        self.assert_emoji('spam', 'mess', '🟨⬜🟨⬜',  
            '"s" occurs only once in the solution, so only one 🟨 is displayed for the "s"')
        
        self.assert_emoji('harass', 'tossed', '⬜⬜🟨🟨⬜⬜',          
            '"s" occurs twice in the solution, so two 🟨 are displayed')

        self.assert_emoji('tossed', 'schuss', '🟨⬜⬜⬜🟨⬜',          
            '"s" occurs only twice in the solution, so only two 🟨 are displayed')

        self.assert_emoji('post', 'mess', '⬜⬜🟩⬜',          
            '"s" occurs only once in the solution and the only occurence is a direct match')

        self.assert_emoji('chill', 'lulls', '🟨⬜⬜🟩⬜',          
            'Second "l" is not displayed as 🟨 because the third one is a direct match')

        self.assert_emoji('xyxxy', 'xxxxz', '🟩⬜🟩🟩⬜',          
            '"x" occurs only three times in the solution, and all occurences are direct matches')
        
    def assert_emoji(self, solution, guess, expected_emoji, message):
        special_game = WordleGame([solution, guess], solution, len(solution), 1, False)
        self.assertEqual(expected_emoji, special_game.guess(guess).to_emoji(), message)

    

unittest.main()

