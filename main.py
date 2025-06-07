import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

class WordScrambleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Word Scramble")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        
        self.word_lists = {
            'Easy': ["apple", "house", "phone", "table", "chair", "bread", "cloud", "water", "pencil", "bottle"],
            'Medium': ["algorithm", "syntax", "binary", "cache", "compiler", "function", "variable", "iteration", "recursion"],
            'Hard': ["machine learning", "quantum computing", "neural network", "cryptography", "parallel processing", "distributed systems"]
        }
        
        self.current_word = ""
        self.scrambled = ""
        self.lives = 3
        self.score = 0
        self.time_left = 30
        self.hints_used = 0
        self.revealed_letters = set()
        
        
        self.create_main_frame()
        self.create_game_frame()
        self.create_score_frame()
        self.show_main_menu()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        
        title = ttk.Label(self.main_frame, text="WORD SCRAMBLE", font=('Times New Roman', 24, 'bold'))
        title.pack(pady=20)
        
        self.difficulty_var = tk.StringVar(value='Medium')
        difficulties = ['Easy', 'Medium', 'Hard']
        for diff in difficulties:
            rb = ttk.Radiobutton(
                self.main_frame, 
                text=diff, 
                variable=self.difficulty_var, 
                value=diff,
                style='Toolbutton'
            )
            rb.pack(pady=5, anchor='w', padx=100)
        
        ttk.Button(
            self.main_frame, 
            text="Start Game", 
            command=self.start_game,
            style='Accent.TButton'
        ).pack(pady=20)
        
        ttk.Button(
            self.main_frame, 
            text="High Scores", 
            command=self.show_high_scores
        ).pack(pady=10)

    def create_game_frame(self):
        self.game_frame = ttk.Frame(self.root)
        
        
        header = ttk.Frame(self.game_frame)
        self.timer_label = ttk.Label(header, text="Time: 30", font=('Times New Roman', 12))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.lives_label = ttk.Label(header, text="Lives: ❤❤❤", font=('Times New Roman', 12))
        self.lives_label.pack(side=tk.RIGHT, padx=10)
        header.pack(fill=tk.X, pady=10)
        
        
        self.scrambled_label = ttk.Label(
            self.game_frame, 
            text="", 
            font=('Times New Roman', 18, 'bold'),
            wraplength=600
        )
        self.scrambled_label.pack(pady=20)
        
        self.guess_entry = ttk.Entry(self.game_frame, font=('Times New Roman', 14))
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', self.check_guess)
        
        btn_frame = ttk.Frame(self.game_frame)
        ttk.Button(btn_frame, text="Submit", command=self.check_guess).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hint", command=self.give_hint).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Quit", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
        btn_frame.pack(pady=10)
        
        self.hint_label = ttk.Label(self.game_frame, text="", foreground='gray')
        self.hint_label.pack(pady=5)

    def create_score_frame(self):
        self.score_frame = ttk.Frame(self.root)
        ttk.Label(self.score_frame, text="High Scores", font=('Times New Roman', 16)).pack(pady=10)
        self.score_list = ttk.Treeview(
            self.score_frame, 
            columns=('rank', 'name', 'score', 'date'), 
            show='headings'
        )
        self.score_list.heading('rank', text='Rank')
        self.score_list.heading('name', text='Name')
        self.score_list.heading('score', text='Score')
        self.score_list.heading('date', text='Date')
        self.score_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        ttk.Button(self.score_frame, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_main_menu(self):
        self.hide_all_frames()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.root.geometry("600x400")

    def start_game(self):
        self.hide_all_frames()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.root.geometry("800x600")

        self.lives = 3
        self.score = 0
        self.time_left = 30
        self.hints_used = 0
        self.revealed_letters = set()

        difficulty = self.difficulty_var.get()
        self.current_word = random.choice(self.word_lists[difficulty]).lower()
        self.scrambled = self.scramble_word(self.current_word)
        self.scrambled_label.config(text=self.scrambled)
        self.guess_entry.delete(0, tk.END)
        self.hint_label.config(text="")
        self.update_lives_display()
        self.start_timer()

    def scramble_word(self, word):
        if ' ' in word:
            return ' '.join(self.scramble_word(w) for w in word.split())
        if len(word) > 3:
            first, *middle, last = word
            random.shuffle(middle)
            return first + ''.join(middle) + last
        return word

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.game_over()

    def update_lives_display(self):
        hearts = '❤' * self.lives
        self.lives_label.config(text=f"Lives: {hearts}")

    def check_guess(self, event=None):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)
        
        if guess == self.current_word:
            self.score += len(self.current_word) * 100 - self.hints_used * 50
            messagebox.showinfo("Correct!", f"Great job! Score: {self.score}")
            self.update_high_scores()
            self.show_main_menu()
        else:
            self.lives -= 1
            self.update_lives_display()
            if self.lives <= 0:
                self.game_over()
            else:
                messagebox.showerror("Wrong", "Incorrect guess! Try again.")

    def give_hint(self):
        if len(self.revealed_letters) < len(set(self.current_word)):
            for letter in self.current_word:
                if letter not in self.revealed_letters and letter.isalpha():
                    self.revealed_letters.add(letter)
                    break
            self.hints_used += 1
            self.hint_label.config(
                text=f"Revealed letters: {' '.join(sorted(self.revealed_letters)).upper()}"
            )
        else:
            messagebox.showinfo("Hints", "No more hints available!")

    def game_over(self):
        messagebox.showinfo("Game Over", 
            f"The word was: {self.current_word}\nYour score: {self.score}")
        self.update_high_scores()
        self.show_main_menu()

    def update_high_scores(self):
        try:
            with open('scores.json', 'r') as f:
                scores = json.load(f)
        except FileNotFoundError:
            scores = []
        
        scores.append({
            'name': "Player",
            'score': self.score,
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        with open('scores.json', 'w') as f:
            json.dump(scores[:10], f)

    def show_high_scores(self):
        self.hide_all_frames()
        self.score_frame.pack(fill=tk.BOTH, expand=True)
        
        for item in self.score_list.get_children():
            self.score_list.delete(item)
        
        try:
            with open('scores.json', 'r') as f:
                scores = json.load(f)
            for i, entry in enumerate(scores[:10], 1):
                self.score_list.insert('', 'end', values=(
                    i, 
                    entry['name'], 
                    entry['score'], 
                    entry['date']
                ))
        except FileNotFoundError:
            pass

    def hide_all_frames(self):
        for frame in [self.main_frame, self.game_frame, self.score_frame]:
            frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordScrambleGame(root)
    root.tk.call('source', 'azure.tcl')
    root.tk.call('set_theme', 'dark')
    root.mainloop()