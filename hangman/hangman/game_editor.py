import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Constants for your Flask API URL
API_BASE_URL = "http://localhost:5001/"  # Adjust this to match your Flask API

class WordEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Phrase Editor")
        self.geometry("750x300")

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

        self.edit_button = tk.Button(self, text="Edit Word", command=self.edit_word_popup)
        self.edit_button.grid(row=1, column=1)

        self.delete_button = tk.Button(self, text="Delete Word", command=self.delete_word)
        self.delete_button.grid(row=1, column=2)

        # Load words initially
        self.load_words()

    def load_words(self):
        """Fetch words from the database via Flask API."""
        try:
            for item in self.word_tree.get_children():
                self.word_tree.delete(item)
            response = requests.get(f"{API_BASE_URL}/getall")
            if response.status_code == 200:
                words = response.json()
                for word in words:
                    self.word_tree.insert("", "end", values=(word["phrase"], word["hint"], word["last_used"]))
            else:
                messagebox.showerror("Error", "Failed to fetch words from the database.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_word_popup(self):
        """Popup for adding a new word."""
        self.edit_popup("Add Phrase", save_callback=self.add_word)

    def edit_word_popup(self):
        """Popup for editing the selected word."""
        selected_word = self.word_tree.selection()
        item_values = self.word_tree.item(selected_word)["values"]
        if selected_word:
            self.edit_popup("Edit Phrase", item_values[0], item_values[1], save_callback=self.edit_word)

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
                                command=lambda: save_callback(word_entry.get(), hint_entry.get(), popup))
        save_button.grid(row=2, column=0, columnspan=2)

    def add_word(self, phrase, hint, popup):
        """Add a word to the database."""
        try:
            response = requests.post(f"{API_BASE_URL}/add", json={"phrase": phrase, "hint": hint})
            if response.status_code == 201:
                self.load_words()
                popup.destroy()
            else:
                messagebox.showerror("Error", "Failed to add phrase.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def edit_word(self, phrase, hint, popup):
        """Edit the selected word in the database."""
        selected_word = self.word_tree.selection()
        if not selected_word:
            return

        try:
            item_values = self.word_tree.item(selected_word)["values"]
            old_phrase = item_values[0]
            response = requests.put(f"{API_BASE_URL}/edit", json={"original_phrase": old_phrase, "phrase": phrase, "hint": hint})
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
            data = {
                "phrase": phrase
            }
            # Send the DELETE request
            response = requests.delete(f"{API_BASE_URL}/delete",json=data)
            if response.status_code == 200:
                self.load_words()
            else:
                messagebox.showerror("Error", "Failed to delete phrase.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Initialize the app
if __name__ == "__main__":
    app = WordEditorApp()
    app.mainloop()