import tkinter as tk
from tkinter import ttk, messagebox
from db_api import HangmanDB_Integration
from llm_api import LLM_Integration

class WordEditorApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Phrase Editor")
        self.geometry("750x300")
        self.db = HangmanDB_Integration()
        self.llm = LLM_Integration()

        # Create a Treeview widget
        self.word_tree = ttk.Treeview(self, columns=("phrase", "hint", "lastused"), show="headings")
        self.word_tree.grid(columnspan=3, row=0, column=0, sticky="nsew")

        # Define the columns
        self.word_tree.heading("phrase", text="Phrase")
        self.word_tree.heading("hint", text="Hint")
        self.word_tree.heading("lastused", text="Last Used")

        # Set column widths
        self.word_tree.column("phrase", width=250)
        self.word_tree.column("hint", width=250)
        self.word_tree.column("lastused", width=250)

        # Buttons for CRUD operations
        self.add_button = tk.Button(self, text="Add Word", command=self.add_word_popup)
        self.add_button.grid(row=1, column=0)

        self.ai_button = tk.Button(self, text="AI Generate Word", command=self.ai_word_popup)
        self.ai_button.grid(row=2, column=0)

        self.edit_button = tk.Button(self, text="Edit Word", command=self.edit_word_popup)
        self.edit_button.grid(row=1, column=1)

        self.delete_button = tk.Button(self, text="Delete Word", command=self.delete_word)
        self.delete_button.grid(row=1, column=2)

        self.protocol("WM_DELETE_WINDOW", self.close)  # Properly handle window close
        self.load_words()

    def close(self):
        """Close the window and release grab."""
        self.grab_release()
        self.destroy()

    def load_words(self):
        """Fetch words from the database via Flask API."""
        for item in self.word_tree.get_children():
            self.word_tree.delete(item)
        words = self.db.getall()
        for word in words:
            self.word_tree.insert("", "end", values=(word["phrase"], word["hint"], word["last_used"]))

    def add_word_popup(self):
        """Popup for adding a new word."""
        self.edit_popup("Add Phrase", save_callback=self.add_word)

    def ai_word_popup(self):
        """Popup for AI Generation of a new word"""
        response = self.llm.getpuzzle()
        hint = response['hint']
        phrase = response['phrase']
        self.edit_popup("Add Phrase", word=phrase, hint=hint, save_callback=self.add_word)

    def edit_word_popup(self):
        """Popup for editing the selected word."""
        selected_word = self.word_tree.selection()
        if selected_word:
            item_values = self.word_tree.item(selected_word)["values"]
            self.edit_popup("Edit Phrase", word=item_values[0], hint=item_values[1], save_callback=self.edit_word)

    def edit_popup(self, title, word=None, hint=None, save_callback=None):
        """Create a popup for adding/editing a word and its hint."""
        popup = tk.Toplevel(self)
        popup.title(title)

        # Word (phrase) field
        tk.Label(popup, text="Phrase:").grid(row=0, column=0)
        word_entry = tk.Entry(popup)
        word_entry.grid(row=0, column=1)
        if word:
            word_entry.insert(0, word)

        # Hint field
        tk.Label(popup, text="Hint:").grid(row=1, column=0)
        hint_entry = tk.Entry(popup)
        hint_entry.grid(row=1, column=1)
        if hint:
            hint_entry.insert(0, hint)

        # Save button
        save_button = tk.Button(popup, text="Save", 
                                command=lambda: self.save_word(save_callback, word_entry.get(), hint_entry.get(), popup))
        save_button.grid(row=2, column=0, columnspan=2)

        popup.transient(self.parent)
        popup.grab_set()
        popup.wm_state('normal')

    def save_word(self, save_callback, phrase, hint, popup):
        """Save the word to the database and close the popup."""
        try:
            save_callback(phrase, hint, popup)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_word(self, phrase, hint, popup):
        """Add a word to the database."""
        response = self.db.add(phrase, hint)
        if response.status_code == 201:
            self.load_words()
            popup.destroy()
        else:
            messagebox.showerror("Error", f"{response.status_code}: {response.text}")

    def edit_word(self, phrase, hint, popup):
        """Edit the selected word in the database."""
        selected_word = self.word_tree.selection()
        if not selected_word:
            return

        try:
            item_values = self.word_tree.item(selected_word)["values"]
            old_phrase = item_values[0]
            response = self.db.edit(old_phrase, phrase, hint)
            if response.status_code == 200:
                self.load_words()
                popup.destroy()
            else:
                messagebox.showerror("Error", "Failed to update phrase.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_word(self):
        """Delete the selected word from the database."""
        selected_word = self.word_tree.selection()
        if not selected_word:
            return

        try:
            item_values = self.word_tree.item(selected_word)["values"]
            phrase = item_values[0]
            response = self.db.delete(phrase)
            if response.status_code == 200:
                self.load_words()
            else:
                messagebox.showerror("Error", "Failed to delete phrase.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
