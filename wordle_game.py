class InvalidWordError(Exception):            
    pass

class OutOfGuessesError(Exception):            
    pass

class GuessResult:
    def __init__(self, is_success, hint):
        self.is_success = is_success
        self.hint = hint

class WordleGame:

    ICON_EXACT_MATCH = '🟩'
    ICON_CONTAINED = '🟨'
    ICON_NOT_CONTAINED = '⬜'

    def __init__(self, words, solution, length, attempts, strict_mode):
        self.words = words
        self.solution = solution
        self.length = length
        self.attempts = attempts
        self.current_attempt = 0
        self.strict_mode = strict_mode

    def guesses_left(self):
        return self.current_attempt < self.attempts
    
    def guess(self, word):        
        if word not in self.words:
            raise InvalidWordError(f'{word} is not a an allowed word')
        elif not self.guesses_left():
            raise OutOfGuessesError('No more guesses left')
        else:
            self.current_attempt += 1
            if word == self.solution:             
                return GuessResult(True, self.ICON_EXACT_MATCH * self.length)
            else:                
                return GuessResult(False, self.get_hint(word))

    def get_hint(self, word):
        result = ''
        for i in range(len(word)):
            if word[i] == self.solution[i]:
                result += self.ICON_EXACT_MATCH
            elif word[i] in self.solution:
                result += self.ICON_CONTAINED
            else:
                result += self.ICON_NOT_CONTAINED
        return result
        
