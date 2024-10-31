'''Hangman game state machine's functions'''

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
        start = re.sub(r'[^ \t\n,.!?;:()\[\]{}]', '_', self._word)
        return self._reveal_letters(start)
    
    def _reveal_letters(self, start):
        end = []
        for index,character in enumerate(self.get_word):
            if start[index] == '_':
                if character in self.guessed_letters:
                    end.append(self.get_word[index])
                else:
                    end.append(start[index])
            if start[index] in ' \t\n,.!?;:()[]{}':
                end.append(start[index])
        return ''.join(end)

    def guess(self, letter):
        returnvalue = False
        if letter in self.guessed_letters:
            print(f"Letter {letter} has already been guessed.  Try again.")
        else:
            self.guessed_letters.append(letter)

            if letter in self.get_word:
                returnvalue = True
                self._display_word = self._calculate_display_word()
                
                # Check if the game is won (all letters guessed)
                if '_' not in self._display_word:
                    self._is_over = True
                    self._is_won = True  # Game is won when all letters are guessed
            else:
                self._remaining_lives = self._remaining_lives - 1
                
                # Check if the game is over (no remaining lives)
                if self.remaining_lives == 0:
                    self._is_over = True
            
        return returnvalue