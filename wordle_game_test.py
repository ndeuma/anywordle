#!/usr/bin/env python3

import unittest
import wordle_game

class WordleGameTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.game = wordle_game.WordleGame(['spam', 'eggs', 'span', 'pain', 'mess'], 'spam', 4, 2, False)

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

    # Implementation detail of original Wordle: When a letter is contained multiple times in the
    # guess, but only once in the solution, a 🟨 is only displayed for the first occurrence
    # in the guess. So, it's 🟨⬜🟨⬜ and not 🟨⬜🟨🟨 here.
    def test_yellow_hint_only_displayed_once_for_every_occurrence_2_vs_1(self):
        result = self.game.guess('mess')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨⬜🟨⬜', result.hint, 
            "'s' gets only one 🟨, because it occurs only once in the solution")        

    def test_yellow_hint_only_displayed_once_for_every_occurrence_2_vs_2(self):
        special_game = wordle_game.WordleGame(['tossed', 'harass'], 'harass', 6, 2, False)
        result = special_game.guess('tossed')
        self.assertFalse(result.is_success)
        self.assertEqual('⬜⬜🟨🟨⬜⬜', result.hint,
            "'s' gets two 🟨, because it occurs twice in the solution")        
    
    def test_yellow_hint_only_displayed_once_for_every_occurrence_3_vs_2(self):
        special_game = wordle_game.WordleGame(['tossed', 'schuss'], 'tossed', 6, 2, False)
        result = special_game.guess('schuss')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨⬜⬜⬜🟨⬜', result.hint,
            "'s' gets only two 🟨, because it occurs only twice in the solution")        

    def test_yellow_hint_only_displayed_once_for_every_occurrence_2_vs_1_overlap_with_green(self):
        special_game = wordle_game.WordleGame(['post', 'mess'], 'post', 4, 2, False)
        result = special_game.guess('mess')
        self.assertFalse(result.is_success)
        self.assertEqual('⬜⬜🟩⬜', result.hint,
            "Second 's' gets no 🟨, because the only occurence of 's' in the solution is already a 🟩")        

    def test_yellow_hint_only_displayed_once_for_every_occurrence_3_vs_2_green_needed(self):
        special_game = wordle_game.WordleGame(['chill', 'lulls'], 'chill', 5, 2, False)
        result = special_game.guess('lulls')
        self.assertFalse(result.is_success)
        self.assertEqual('🟨⬜⬜🟩⬜', result.hint,
            "'l' gets only one 🟨 because it occurs only twice in the solution, and the later 🟩 takes precedence")

unittest.main()

