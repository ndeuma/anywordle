#!/usr/bin/env python3

import unittest
import wordle_game

class WordleGameTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.game = wordle_game.WordleGame(['spam', 'eggs', 'span', 'pain'], 'spam', 4, 2, False)

    def test_init(self):        
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(0, self.game.current_attempt)

    def test_word_too_long(self):
        with self.assertRaises(wordle_game.InvalidWordError):
            self.game.guess('spain')

    def test_word_not_existing(self):
        with self.assertRaises(wordle_game.InvalidWordError):
            self.game.guess('spal')

    def test_too_many_guesses(self):
        self.game.guess('pain')
        self.game.guess('pain')
        with self.assertRaises(wordle_game.OutOfGuessesError):
            self.game.guess('pain')

    def test_guess_correct(self):        
        result = self.game.guess('spam')
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
        result = self.game.guess('pain')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨🟨⬜⬜', result.hint)
        self.assertEqual(True, self.game.guesses_left())
        self.assertEqual(1, self.game.current_attempt)

unittest.main()

