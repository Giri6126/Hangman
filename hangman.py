import tkinter as tk
from tkinter import messagebox
import random
#HK
# ---------------- Word Categories & Hints ----------------
categories = {
    "fruits": ["apple", "banana", "mango", "orange"],
    "animals": ["elephant", "giraffe", "tiger", "kangaroo"],
    "tech": ["computer", "python", "keyboard", "monitor"]
}

hints = {
    "apple": "A fruit that keeps the doctor away",
    "banana": "A long yellow fruit",
    "mango": "King of fruits",
    "orange": "A citrus fruit",
    "elephant": "Largest land animal",
    "giraffe": "Tallest land animal",
    "tiger": "Big striped cat",
    "kangaroo": "Animal that jumps with a pouch",
    "computer": "Used to code or browse",
    "python": "Programming language or a snake",
    "keyboard": "Used to type on a computer",
    "monitor": "Displays visuals from a computer"
}

MAX_WRONG = 6  # Maximum wrong guesses

# ---------------- Main Hangman Game Class ----------------
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Hangman Game")
        self.root.geometry("800x500")
        self.root.config(bg="#F0F4F8")

        # Canvas for Hangman
        self.canvas = tk.Canvas(root, width=250, height=300, bg="#E8EAF6", highlightthickness=0)
        self.canvas.place(x=520, y=50)

        # Category selection
        self.category_label = tk.Label(root, text="Choose Category: fruits, animals, tech", font=("Helvetica", 12, "bold"), bg="#F0F4F8")
        self.category_label.place(x=20, y=20)
        self.category_entry = tk.Entry(root, font=("Helvetica", 12))
        self.category_entry.place(x=300, y=20)

        self.start_btn = tk.Button(root, text="Start Game", command=self.start_game, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), width=12)
        self.start_btn.place(x=550, y=17)

        # Word display
        self.word_label = tk.Label(root, text="", font=("Helvetica", 28, "bold"), bg="#F0F4F8", fg="#1A237E")
        self.word_label.place(x=20, y=80)

        # Hint
        self.hint_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), fg="#D32F2F", bg="#F0F4F8")
        self.hint_label.place(x=20, y=140)

        # Letter buttons
        self.buttons_frame = tk.Frame(root, bg="#F0F4F8")
        self.buttons_frame.place(x=20, y=180)
        self.letter_buttons = {}

        # Replay Button
        self.replay_btn = tk.Button(root, text="Replay", command=self.replay_game, bg="#FF5722", fg="white", font=("Helvetica", 12, "bold"), width=12)
        self.replay_btn.place(x=320, y=450)

        self.reset_game_variables()

    # ---------------- Reset Variables ----------------
    def reset_game_variables(self):
        self.word = ""
        self.display_word = []
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.game_active = False
        self.canvas.delete("all")
        self.word_label.config(text="")
        self.hint_label.config(text="")
        # Destroy previous buttons
        for btn in self.letter_buttons.values():
            btn.destroy()
        self.letter_buttons = {}

    # ---------------- Start Game ----------------
    def start_game(self):
        category = self.category_entry.get().lower()
        if category not in categories:
            messagebox.showinfo("Info", "Invalid category! Defaulting to 'fruits'.")
            category = "fruits"

        self.word = random.choice(categories[category])
        self.display_word = ["_"] * len(self.word)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.game_active = True

        self.update_word_label()
        self.hint_label.config(text="")

        # Create letter buttons with colors
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, height=2,
                            command=lambda l=letter: self.guess_letter(l.lower()),
                            bg="#1976D2", fg="white", font=("Helvetica", 10, "bold"))
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#64B5F6"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1976D2"))
            self.letter_buttons[letter] = btn

    # ---------------- Handle Letter Guess ----------------
    def guess_letter(self, letter):
        if not self.game_active:
            return
        if letter in self.guessed_letters:
            return
        self.guessed_letters.append(letter)
        self.letter_buttons[letter.upper()].config(state="disabled", bg="#B0BEC5")

        if letter in self.word:
            for i, l in enumerate(self.word):
                if l == letter:
                    self.display_word[i] = letter
            self.update_word_label()
            if "_" not in self.display_word:
                messagebox.showinfo("🎉 Hangman", f"Congratulations! You guessed the word: {self.word}")
                self.game_active = False
        else:
            self.wrong_guesses += 1
            self.draw_hangman()
            if self.wrong_guesses == MAX_WRONG // 2 and self.word in hints:
                self.hint_label.config(text=f"Hint: {hints[self.word]}")
            if self.wrong_guesses >= MAX_WRONG:
                messagebox.showinfo("💀 Hangman", f"Game Over! The word was: {self.word}")
                self.game_active = False

    # ---------------- Update Word Display ----------------
    def update_word_label(self):
        self.word_label.config(text=" ".join(self.display_word))

    # ---------------- Draw Hangman ----------------
    def draw_hangman(self):
        self.canvas.delete("all")
        # Gallows
        self.canvas.create_line(50, 250, 150, 250, width=3, fill="#3E2723")
        self.canvas.create_line(100, 250, 100, 50, width=3, fill="#3E2723")
        self.canvas.create_line(100, 50, 200, 50, width=3, fill="#3E2723")
        self.canvas.create_line(200, 50, 200, 70, width=3, fill="#3E2723")

        # Hangman based on wrong_guesses
        if self.wrong_guesses >= 1:
            self.canvas.create_oval(180, 70, 220, 110, width=3, outline="#D32F2F")  # Head
        if self.wrong_guesses >= 2:
            self.canvas.create_line(200, 110, 200, 170, width=3, fill="#D32F2F")  # Body
        if self.wrong_guesses >= 3:
            self.canvas.create_line(200, 120, 170, 150, width=3, fill="#D32F2F")  # Left arm
        if self.wrong_guesses >= 4:
            self.canvas.create_line(200, 120, 230, 150, width=3, fill="#D32F2F")  # Right arm
        if self.wrong_guesses >= 5:
            self.canvas.create_line(200, 170, 170, 200, width=3, fill="#D32F2F")  # Left leg
        if self.wrong_guesses >= 6:
            self.canvas.create_line(200, 170, 230, 200, width=3, fill="#D32F2F")  # Right leg

    # ---------------- Replay Game ----------------
    def replay_game(self):
        self.reset_game_variables()

# ---------------- Main Program ----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
