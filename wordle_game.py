import ansi_escape
from enum import Enum
import re
from string import ascii_uppercase

class LetterStatus(Enum):
    EXACT_MATCH = 0,
    CONTAINED = 1,
    NOT_CONTAINED = 2

class InvalidWordError(Exception):            
    pass

class OutOfGuessesError(Exception):            
    pass

class InvalidInStrictModeError(Exception):            
    pass

class GuessResult:
    def __init__(self, is_success, hint):
        self.is_success = is_success
        self.hint = hint

    def to_emoji(self):
        result = ''
        for letter_info in self.hint:
            if letter_info[1] == LetterStatus.EXACT_MATCH:
                result += '🟩'
            elif letter_info[1] == LetterStatus.CONTAINED:
                result += '🟨'
            else:
                result += '⬜'
        return result

class WordleGame:

    ICON_EXACT_MATCH = '🟩'
    ICON_CONTAINED = '🟨'
    ICON_NOT_CONTAINED = '⬜'

    NO_ERROR = ''

    def __init__(self, words, solution, length, attempts, strict_mode):
        self.words = words
        self.solution = solution
        self.length = length
        self.attempts = attempts
        self.attempts_made = 0
        self.strict_mode = strict_mode
        self.exact_match_letters_by_position = {}
        self.contained_letters = set()
        self.excluded_letters = set()

    def guesses_left(self):
        return self.attempts_made < self.attempts
    
    def guess(self, word):        
        word_lower = word.lower()
        if word_lower not in self.words:
            raise InvalidWordError(f'{word} is not an allowed word')
        elif not self.guesses_left():
            raise OutOfGuessesError('No more guesses left')        
        else:
            if (self.strict_mode):
                strict_mode_error = self.get_validation_error(word)
                if (strict_mode_error != self.NO_ERROR):
                    raise InvalidInStrictModeError(strict_mode_error)            
            self.attempts_made += 1            
            result = GuessResult(word_lower == self.solution, self.get_hint(word_lower))
            if not result.is_success:
                self.update_letter_hints(word_lower, result)
            return result

    def get_hint(self, word):
        result = []
        for i in range(len(word)):
            if word[i] == self.solution[i]:
                result.append((word[i], LetterStatus.EXACT_MATCH))
            elif word[i] in self.solution:
                if self.has_more_occurrences_up_to(i, word):
                    result.append((word[i], LetterStatus.NOT_CONTAINED))
                else:
                    result.append((word[i], LetterStatus.CONTAINED))
            else:
                result.append((word[i], LetterStatus.NOT_CONTAINED))
        return result

    def has_more_occurrences_up_to(self, index, guess):
        letter = guess[index] 
        exact_matches = 0
        occurrences_in_guess = 0
        occurrences_in_solution = 0        
        for i in range(len(self.solution)):
            if (guess[i] == letter and self.solution[i] == letter):
                exact_matches += 1
            if (guess[i] == letter and i <= index):
                occurrences_in_guess += 1
            if (self.solution[i] == letter):
                occurrences_in_solution += 1
        return occurrences_in_guess > occurrences_in_solution - exact_matches
    
    def get_validation_error(self, guess):        
        for i in range(len(guess)):
            if (i in self.exact_match_letters_by_position and self.exact_match_letters_by_position[i] != guess[i]):
                return f'The letter at position {i+1} must be {self.exact_match_letters_by_position[i]}'
        missing_chars = sorted(list(filter(lambda c: c not in guess, self.contained_letters)))
        if len(missing_chars) > 0:
            return f'The following letters must be contained in the guess: {", ".join(missing_chars)}'
        return self.NO_ERROR

    def update_letter_hints(self, guess, result):
        for i in range(len(result.hint)):
            letter = result.hint[i][0]
            status = result.hint[i][1]
            if status == LetterStatus.EXACT_MATCH:
                self.exact_match_letters_by_position[i] = letter
                if letter in self.contained_letters:
                    self.contained_letters.remove(letter)
            elif status == LetterStatus.CONTAINED:
                self.contained_letters.add(letter)
            else:
                self.excluded_letters.add(letter)

    def get_keyboard(self):
        result = ''
        for c in ascii_uppercase:
            if c.lower() in self.exact_match_letters_by_position.values():    
                result += ansi_escape.color_text_256(255, 34, c)
            elif c.lower() in self.contained_letters:
                result += ansi_escape.color_text_256(0, 11, c)
            elif c.lower() in self.excluded_letters:
                result += ' '
            else:
                result += c
        return result

    
        

        

