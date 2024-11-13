import tkinter as tk
from tkinter import Menu

from game_editor import WordEditorApp
from gameboard import GameWindow
from db_api import HangmanDB_Integration
from game import Hangman

# Define your app
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman")
        self.withdraw()
        self.create_menu()
        self.db_integration = HangmanDB_Integration()  # Instantiate your DB integration
        # Initialize the game board as the main application window
        self.game_board = None
        self.new_game()

    def create_menu(self):
        # Create a menu bar
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Phrase Editor", command=self.open_game_editor)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def open_game_editor(self):
        editor = WordEditorApp(self)  # Pass self as parent
        editor.grab_set()  # Make editor modal
        editor.wait_window()  # Wait for editor to close
        editor.destroy() 

    def quit_app(self):
        # Close the entire application
        self.quit()

    def new_game(self):
        word = self.db_integration.random()
        self.game_state = Hangman(word.json()['phrase'])
        self.hint = word.json()['hint']
        
        # Open the game modal window
        self.game_board = GameWindow(self.game_state, self.hint, self.db_integration)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()