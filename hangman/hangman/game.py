'''Hangman game functions'''

import re

class Hangman:
    def __init__(self, word):
        '''Create a new Hangman game where [word] is the word or phrase the player is trying to guess.'''
        self._remaining_lives = 6
        self._guessed_letters = []
        self._is_over = False
        self._is_won = False
        self._word = word.upper()

        self._display_word = self._calculate_display_word()
    
    @property
    def remaining_lives(self):
        return self._remaining_lives
    
    @property
    def guessed_letters(self):
        return self._guessed_letters
    
    @property
    def game_over(self):
        return self._is_over
    
    @property
    def game_won(self):
        return self._is_won
    
    @property
    def get_word(self):
        return self._word
    
    @property
    def get_display_word(self):
        return self._display_word
    
    def _calculate_display_word(self):
        '''Starting with a series of underscores that represent the letters in a word/phrase, fill in the blanks with the letters that have already been guessed.'''
        return re.sub(r'[a-zA-Z0-9]', '_', self._word)