import random
from .exceptions import *


class GuessAttempt(object):
# Checks if the player a valid guess attempt. This class is not checking if the attempt is in the masked word.
    def __init__(self, letter, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()
        
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit is True:
            return True
        return False
            
    def is_miss(self):
        if self.miss is True:
            return True
        return False
        
class GuessWord(object):
# This class keeps track of the word to guess and current state of the masked word.
    def __init__(self, answer):
        if not answer:
            raise InvalidWordException()
        self.answer = answer
        self.masked = '*' * len(self.answer)
    
# Current code passes first three tests. Struggling to figure out how to use the GuessAttempt class successfully and check if guessed letter is in answer 
    def unveil_word(self, letter):
        new_word = ''
        for i in range(len(self.answer)):
            answer_char = self.answer[i]
            mask_char = self.masked[i]
            if mask_char != '*':
                new_word += mask_char
            elif letter == answer_char.lower():
                new_word += answer_char.lower()
            else:
                new_word += '*'
        return new_word
        
    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        letter = letter.lower()
        
        attempt = GuessAttempt(letter)
        if letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unveil_word(letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        word_to_guess = self.select_random_word(word_list)
        self.word = GuessWord(word_to_guess)
        self.previous_guesses = []
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
    
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        self.previous_guesses.append(letter.lower())
        
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        
        if self.is_won():
            raise GameWonException()
            
        return attempt
        
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    

    