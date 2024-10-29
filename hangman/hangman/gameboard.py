import tkinter as tk
from tkinter import messagebox
from game import Hangman
from db_api import HangmanDB_Integration

class GameWindow(tk.Toplevel):
    def __init__(self, game_state, hint, db_integration):
        super().__init__()
        self.game_state = game_state
        self.db = db_integration  # Integrate database functionality
        self.title("Hangman Game")
        self.geometry("400x400")
        self.grab_set()  # Make this window modal

        # Display word
        self.word_label = tk.Label(self, text=self.game_state.get_display_word, font=("Helvetica", 16))
        self.word_label.pack(pady=10)
        
        # Display remaining lives
        self.lives_label = tk.Label(self, text=f"Lives: {self.game_state.remaining_lives}", font=("Helvetica", 14))
        self.lives_label.pack(pady=5)
        
        # Display guessed letters
        self.hint_label = tk.Label(self, text=f"Hint: {hint}", font=("Helvetica", 10))
        self.hint_label.pack(pady=5)

        # Display guessed letters
        self.guessed_label = tk.Label(self, text=f"Guessed Letters: {', '.join(self.game_state.guessed_letters)}", font=("Helvetica", 10))
        self.guessed_label.pack(pady=5)
        
        # Input for guessing a letter
        self.guess_entry = tk.Entry(self, font=("Helvetica", 14))
        self.guess_entry.pack(pady=10)
        
        # Submit button
        self.submit_button = tk.Button(self, text="Guess", command=self.make_guess)
        self.submit_button.pack(pady=5)
        
        # Quit button
        self.quit_button = tk.Button(self, text="Close", command=self.destroy)
        self.quit_button.pack(pady=5)
        
        # Feedback area
        self.feedback_label = tk.Label(self, text="", font=("Helvetica", 10), fg="red")
        self.feedback_label.pack(pady=5)

    def make_guess(self):
        letter = self.guess_entry.get().upper()
        if len(letter) != 1 or not letter.isalpha():
            self.feedback_label.config(text="Please enter a single letter.")
            return
        
        # Process the guess and save to the database
        correct = self.game_state.guess(letter)

        # Update display after each guess
        self.word_label.config(text=self.game_state.get_display_word)
        self.lives_label.config(text=f"Lives: {self.game_state.remaining_lives}")
        self.guessed_label.config(text=f"Guessed Letters: {', '.join(self.game_state.guessed_letters)}")

        # Check if the game has ended
        if self.game_state.game_over:
            if self.game_state.game_won:
                messagebox.showinfo("Game Over", "Congratulations, you've won!")
            else:
                messagebox.showinfo("Game Over", f"You've lost! The word was: {self.game_state.get_word}")
            self.disable_widgets()
            return
        
        # Feedback for guess outcome
        self.feedback_label.config(text="Correct!" if correct else "Incorrect guess.")
        self.guess_entry.delete(0, tk.END)

    def disable_widgets(self):
        """Disables all widgets on the game board screen."""
        self.widgets_disabled = True
        for widget in self.board.winfo_children():
            if isinstance(widget, (tk.Entry, tk.Button, tk.Label)):
                widget.config(state="disabled")
                # Prevent focus events on Entry widgets
                if isinstance(widget, tk.Entry):
                    widget.bind("<FocusIn>", lambda e: "break")

    def enable_widgets(self):
        """Re-enables all widgets on the game board screen."""
        self.widgets_disabled = False
        for widget in self.board.winfo_children():
            if isinstance(widget, (tk.Entry, tk.Button, tk.Label)):
                widget.config(state="normal")
                # Re-enable focus events on Entry widgets
                if isinstance(widget, tk.Entry):
                    widget.unbind("<FocusIn>")

# Usage Example within GameBoard class
class GameBoard:
    def __init__(self, root, open_editor_callback):
        self.root = root
        
        # Initialize game state and database
        self.db_integration = HangmanDB_Integration()  # Instantiate your DB integration
        word = self.db_integration.random()
        self.game_state = Hangman(word.json()['phrase'])
        self.hint = word.json()['hint']
        
        # Open the game modal window
        GameWindow(self.game_state, self.hint, self.db_integration)