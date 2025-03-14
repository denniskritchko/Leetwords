import tkinter as tk
from tkinter import messagebox, scrolledtext, Frame, Label, Button, Entry, StringVar
import random
import string
import os
import json
from collections import defaultdict
import time
import traceback
import tkinter.ttk as ttk

class CrosswordGenerator:
    def __init__(self, dictionary_path=None):
        # Load dictionary or use default words
        self.words_by_length = defaultdict(list)
        self.clues = {}
        self.load_dictionary(dictionary_path)
        
        # Grid properties
        self.grid = {}  # (row, col) -> letter
        self.word_list = []  # (word, row, col, horizontal)
        self.debug_info = []
        
        # Track grid boundaries
        self.min_row = float('inf')
        self.max_row = float('-inf')
        self.min_col = float('inf')
        self.max_col = float('-inf')
    
    def load_dictionary(self, dictionary_path):
        """Load words and clues from a dictionary file"""
        try:
            if dictionary_path and os.path.exists(dictionary_path):
                print(f"Loading dictionary from: {dictionary_path}")
                with open(dictionary_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or ':' not in line:
                            continue
                        word, clue = line.split(':', 1)
                        word = word.strip().upper()
                        clue = clue.strip()
                        if len(word) >= 3 and all(c.isalpha() for c in word):
            self.words_by_length[len(word)].append(word)
            self.clues[word] = clue
                print(f"Loaded {sum(len(words) for words in self.words_by_length.values())} words")
            else:
                print(f"Dictionary file not found: {dictionary_path}")
                print(f"Current working directory: {os.getcwd()}")
                raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")
        except Exception as e:
            print(f"Error loading dictionary: {str(e)}")
            raise

    def generate_crossword(self, min_words=10):
        """Generate a crossword puzzle"""
        self.create_empty_grid()
        
        # Check if we have any words
        if not any(self.words_by_length.values()):
            self.debug_info.append("No words available in dictionary")
            return False
        
        # Get all available lengths
        available_lengths = sorted(self.words_by_length.keys(), reverse=True)
        
        # Place first word at (0, 0)
        first_length = available_lengths[0]
        first_word = random.choice(self.words_by_length[first_length])
        if not self.place_word(first_word, 0, 0, True):
            return False
        
        used_words = {first_word}
        attempts = 0
        max_attempts = 1000
        
        while len(self.word_list) < min_words and attempts < max_attempts:
            attempts += 1
            
            # Choose a random existing word to build from
            ref_word, ref_row, ref_col, ref_horizontal = random.choice(self.word_list)
            
            # Try to place a word intersecting with the reference word
            for ref_pos in range(len(ref_word)):
            letter = ref_word[ref_pos]
            
                # Calculate intersection position
            if ref_horizontal:
                pos_row, pos_col = ref_row, ref_col + ref_pos
            else:
                pos_row, pos_col = ref_row + ref_pos, ref_col
            
                # Try placing a word perpendicular to reference word
                direction = not ref_horizontal
            
                # Try each available length
                for length in available_lengths:
                if length <= 2:  # Skip very short words
                    continue
                    
                    candidates = [w for w in self.words_by_length[length]
                                if w not in used_words and letter in w]
                    
                    if not candidates:
                        continue
                        
                    # Try each candidate word
                    for word in random.sample(candidates, min(len(candidates), 5)):
                        # Find where the matching letter appears in the word
                        for i, char in enumerate(word):
                            if char != letter:
                                continue
                                
                            # Calculate start position
                            if direction:  # Vertical
                                start_row = pos_row - i
                                start_col = pos_col
                            else:  # Horizontal
                                start_row = pos_row
                                start_col = pos_col - i
                            
                            if self.can_place_word(word, start_row, start_col, direction):
                                if self.place_word(word, start_row, start_col, direction):
                                    used_words.add(word)
                                    break
                        
        return len(self.word_list) >= min_words

    def create_empty_grid(self):
        """Initialize an empty grid"""
        self.grid = {}
        self.word_list = []
        self.debug_info = []
        self.min_row = float('inf')
        self.max_row = float('-inf')
        self.min_col = float('inf')
        self.max_col = float('-inf')
    
    def get_letter(self, row, col):
        """Get letter at position, return space if empty"""
        return self.grid.get((row, col), ' ')
    
    def toggle_cell(self, row, col):
        """Toggle a cell between active (white) and inactive (black)"""
        if (row, col) in self.grid:
            del self.grid[(row, col)]
            else:
            self.grid[(row, col)] = ''
            # Update grid boundaries
            self.min_row = min(self.min_row, row)
            self.max_row = max(self.max_row, row)
            self.min_col = min(self.min_col, col)
            self.max_col = max(self.max_col, col)


class CrosswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Generator")
        
        # Get the directory where the script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Dictionary mapping with absolute paths
        self.dictionaries = {
            "Standard Dictionary": os.path.join(self.script_dir, "dictionary.txt"),
            "Internet Lingo": os.path.join(self.script_dir, "internetlingo.txt")
        }
        
        # Create the crossword generator with default dictionary
        default_dict = self.dictionaries["Standard Dictionary"]
        print(f"Loading default dictionary from: {default_dict}")  # Debug print
        self.generator = CrosswordGenerator(default_dict)
        
        # Canvas properties
        self.cell_size = 40
        self.canvas_width = 800
        self.canvas_height = 600
        self.offset_x = self.canvas_width // 2
        self.offset_y = self.canvas_height // 2
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Control panel
        control_panel = ttk.Frame(self.root, padding="5")
        control_panel.pack(fill=tk.X)
        
        # Dictionary selector
        dict_frame = ttk.LabelFrame(control_panel, text="Dictionary", padding="5")
        dict_frame.pack(side=tk.LEFT, padx=5)
        
        self.dict_var = tk.StringVar(value="Standard Dictionary")
        dict_selector = ttk.Combobox(dict_frame, textvariable=self.dict_var, 
                                   values=list(self.dictionaries.keys()),
                                   state="readonly", width=20)
        dict_selector.pack(side=tk.LEFT)
        
        # Generate button
        generate_btn = ttk.Button(control_panel, text="Generate Crossword", 
                                command=self.generate_crossword)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Canvas for crossword display
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, 
                              height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def generate_crossword(self):
        """Generate a new crossword puzzle"""
        # Load the selected dictionary
        selected_dict = self.dictionaries[self.dict_var.get()]
        self.generator = CrosswordGenerator(selected_dict)
        
        if self.generator.generate_crossword(min_words=10):
            self.redraw_crossword()
        else:
            messagebox.showerror("Error", "Failed to generate crossword")
    
    def redraw_crossword(self):
        """Redraw the crossword puzzle"""
        self.canvas.delete("all")
        
        # Draw cells
        for (row, col), letter in self.generator.grid.items():
            x = self.offset_x + col * self.cell_size
            y = self.offset_y + row * self.cell_size
            
            # Draw cell background
            self.canvas.create_rectangle(x, y, x + self.cell_size, 
                                      y + self.cell_size, fill='white', 
                                      outline='black')
            
            # Draw letter
            self.canvas.create_text(x + self.cell_size/2, 
                                  y + self.cell_size/2,
                                  text=letter, font=('Arial', 14, 'bold'))

if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordApp(root)
    root.mainloop()