import tkinter as tk
from tkinter import Menu, Toplevel

from game_editor import WordEditorApp
from gameboard import GameBoard

# Define your app
class MainApp:
    def __init__(self, root):
        self.root = root
        self.create_menu()

        # Initialize the game board as the main application window
        self.game_board = GameBoard(self.root, self.open_game_editor)

    def create_menu(self):
        # Create a menu bar
        menu_bar = Menu(self.root)

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

        # Configure the window to use this menu
        self.root.config(menu=menu_bar)

    def open_game_editor(self):
        # Open the game editor as a modal
        WordEditorApp(self.game_board.board)

    def quit_app(self):
        # Close the entire application
        self.root.quit()

    def new_game(self):
        # Initialize the game board as the main application window
        if self.game_board:
            self.game_board = GameBoard(self.root, self.open_game_editor)

# Entry point of the application
def main():
    root = tk.Tk()
    root.withdraw()  # Hide root window since GameBoard acts as the main window
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()