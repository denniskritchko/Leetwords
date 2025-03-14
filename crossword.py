import tkinter as tk
from tkinter import messagebox, scrolledtext, Frame, Label, Button, Entry, StringVar
import random
import string
import os
import json
from collections import defaultdict
import time
import traceback

class CrosswordGenerator:
    def __init__(self, dictionary_path=None):
        # Load dictionary or use default words
        self.words_by_length = defaultdict(list)
        self.clues = {}
        if dictionary_path and os.path.exists(dictionary_path):
            try:
                with open(dictionary_path, 'r') as f:
                    words = [word.strip().upper() for word in f.readlines()]
                    for word in words:
                        if len(word) >= 3 and all(c.isalpha() for c in word):
                            self.words_by_length[len(word)].append(word)
            except Exception as e:
                print(f"Error loading dictionary: {e}")
                self._load_default_words()
        else:
            self._load_default_words()
        
        # Grid properties
        self.size = 15  # Default grid size
        self.grid = None
        self.word_list = []
        self.clues = {}
        self.debug_info = []
        
    # ... existing code ...

    def _load_default_words(self):
        # Default word list with witty clues
        default_words_and_clues = {
            "PYTHON": "Snake that writes code instead of biting",
            "PUZZLE": "Brain teaser that makes you feel both smart and dumb",
            "ALGORITHM": "Recipe for computers that never includes salt",
            "GENERATOR": "Factory that makes things without coffee breaks",
            "CROSSWORD": "Word maze that makes you question your vocabulary",
            "CODE": "Modern poetry that only computers truly appreciate",
            "PROGRAMMING": "Art of telling a computer exactly what you want, only to get what you asked for",
            "SOFTWARE": "Stuff that turns coffee into computer instructions",
            "DEVELOPER": "Professional googler with coding skills",
            "COMPUTER": "Electronic brain that does what you tell it, not what you want",
            "FUNCTION": "Code container that promises to return something... eventually",
            "VARIABLE": "Digital box that never stays constant",
            "CLASS": "Blueprint for objects that sometimes skip their constructor",
            "OBJECT": "Instance of reality in a virtual world",
            "METHOD": "Function that belongs to a class but acts independently",
            "INTERFACE": "Contract that everyone agrees to implement but nobody reads",
            "LIBRARY": "Collection of code that someone else wrote so you don't have to",
            "PACKAGE": "Bundle of code that hopes to be imported",
            "MODULE": "Code file that thinks it's special enough to be imported",
            "SYSTEM": "Complex arrangement that works by magic until it doesn't",
            "DATA": "Information that's worth more than the computer storing it",
            "STRUCTURE": "Organization system that makes sense until you need to modify it",
            "ARRAY": "List that knows math",
            "LIST": "Array that went to liberal arts school",
            "DICTIONARY": "Key-value relationship counselor",
            "STACK": "Pile of data that follows 'last in, first out' like a cat",
            "QUEUE": "Line of data that actually follows the rules",
            "TREE": "Data structure that grows downward",
            "GRAPH": "Network of nodes that's not on social media",
            "SEARCH": "Hide and seek champion of algorithms",
            "SORT": "Process of organizing data that always takes longer than you think",
            "RECURSION": "See 'recursion'",
            "ITERATION": "Loop that promises to end... eventually",
            "LOOP": "Code's way of saying 'again, again!'",
            "DEBUG": "Detective work for code crimes",
            "ERROR": "Computer's way of saying 'you messed up'",
            "EXCEPTION": "Unexpected party crasher in your code",
            "APP": "Program that thinks it's too cool to be called a program",
            "WEB": "Spider's creation that caught the whole world",
            "GAME": "Interactive entertainment that eats your time",
            "FILE": "Digital drawer that never gets full",
            "USER": "Person who expects computers to read minds",
            "VIEW": "Window to your data's soul",
            "FORM": "Digital paperwork that still feels like paperwork",
            "TEXT": "Letters that computers pretend to understand",
            "EDIT": "Digital eraser and pencil dance",
            "SAVE": "Ctrl+S reflex action",
            "HELP": "Documentation that you read only when desperate",
            "TOOL": "Digital Swiss Army knife",
            "MENU": "List of options you'll explore only once",
            "BYTE": "Eating a 0 or 1",
            "WORD": "Group of bytes having a meeting",
            "TYPE": "Category that doesn't like surprises",
            "NAME": "Label that follows conventions until it doesn't",
            "CALL": "Function's dinner bell",
            "LINK": "Digital handshake between files",
            "HOST": "Computer that opens its ports to strangers",
            "PORT": "Digital doorway that firewalls love to block",
            "TIME": "Resource that debugging consumes most",
            "DATE": "Calendar entry that causes bugs across time zones",
            "MATH": "Universal language that computers actually understand",
            "GRID": "Excel's favorite playground",
            "CELL": "Grid's smallest room",
            "LINE": "Code that hopes to be executed",
            "DRAW": "Pixel painter's paradise",
            "FONT": "Digital fashion for letters"
        }

        # Add words to the dictionary
        for word, clue in default_words_and_clues.items():
            self.words_by_length[len(word)].append(word)
            self.clues[word] = clue

        # Add short words with witty clues
        short_words_and_clues = {
            "AND": "Boolean matchmaker",
            "THE": "Article that demands attention",
            "FOR": "Loop's favorite word",
            "BUT": "Exception's favorite word",
            "NOT": "Boolean opposite day",
            "ALL": "Collection's group hug",
            "ANY": "Database's wild card",
            "NEW": "Object's birthday moment",
            "OLD": "Legacy code's status",
            "BIG": "Data's size problem",
            "RED": "Error message's favorite color",
            "SUN": "Star that doesn't run Java",
            "CAT": "Unix command or internet's favorite animal",
            "DOG": "Loyal debugger",
            "HAT": "White or black, hacker's choice",
            "CAR": "Object that drives classes",
            "RUN": "Command that crosses fingers",
            "SEE": "Visual bug hunting",
            "EAT": "What bugs do to memory",
            "USE": "Import's reason for being",
            "GET": "Getter's only job",
            "PUT": "Setter's daily task",
            "TRY": "Block that expects failure",
            "SAY": "Console's voice",
            "ASK": "Input's invitation",
            "YES": "Boolean's optimistic view",
            "NO": "Boolean's pessimistic view"
        }

        # Add short words
        for word, clue in short_words_and_clues.items():
            self.words_by_length[len(word)].append(word)
            self.clues[word] = clue

    def set_size(self, size):
        """Set the size of the crossword grid"""
        self.size = max(10, min(size, 25))  # Limit size between 10 and 25
    
    def create_empty_grid(self):
        """Initialize an empty grid"""
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.word_list = []
        # Save the existing clues
        saved_clues = self.clues.copy()
        self.clues = saved_clues  # Restore the clues instead of clearing them
        self.debug_info = []
    
    def can_place_word(self, word, row, col, horizontal):
        """Check if a word can be placed at the given position"""
        length = len(word)
        
        # Check boundaries
        if horizontal and col + length > self.size:
            return False
        if not horizontal and row + length > self.size:
            return False
        
        # Check for negative indices
        if row < 0 or col < 0:
            return False
        
        intersections = 0
        for i in range(length):
            r, c = row, col
            if horizontal:
                c += i
            else:
                r += i
            
            # Check if position is valid
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
                
            # Check if the cell already contains a letter
            if self.grid[r][c] != ' ' and self.grid[r][c] != word[i]:
                return False
            
            # Count intersections
            if self.grid[r][c] == word[i]:
                intersections += 1
                
            # Check adjacent cells (no touching words allowed except at intersections)
            if horizontal:
                # Check above and below
                if r > 0 and self.grid[r-1][c] != ' ' and (i == 0 or i == length-1 or self.grid[r][c] == ' '):
                    return False
                if r < self.size-1 and self.grid[r+1][c] != ' ' and (i == 0 or i == length-1 or self.grid[r][c] == ' '):
                    return False
                
                # Check left edge
                if i == 0 and c > 0 and self.grid[r][c-1] != ' ':
                    return False
                
                # Check right edge
                if i == length-1 and c < self.size-1 and self.grid[r][c+1] != ' ':
                    return False
            else:
                # Check left and right
                if c > 0 and self.grid[r][c-1] != ' ' and (i == 0 or i == length-1 or self.grid[r][c] == ' '):
                    return False
                if c < self.size-1 and self.grid[r][c+1] != ' ' and (i == 0 or i == length-1 or self.grid[r][c] == ' '):
                    return False
                
                # Check top edge
                if i == 0 and r > 0 and self.grid[r-1][c] != ' ':
                    return False
                
                # Check bottom edge
                if i == length-1 and r < self.size-1 and self.grid[r+1][c] != ' ':
                    return False
        
        # For non-first word, require at least one intersection
        if len(self.word_list) > 0 and intersections == 0:
            return False
            
        return True
    
    def place_word(self, word, row, col, horizontal, clue=""):
        """Place a word on the grid"""
        try:
            for i, letter in enumerate(word):
                if horizontal:
                    self.grid[row][col + i] = letter
                else:
                    self.grid[row + i][col] = letter
            
            self.word_list.append((word, row, col, horizontal))
            if clue:
                self.clues[word] = clue
                
        except Exception as e:
            self.debug_info.append(f"Error placing word {word} at ({row}, {col}): {str(e)}")
            return False
        return True
    
    def generate_clue(self, word):
        """Generate a simple clue for a word"""
        # Dictionary of simple clues for demonstration
        sample_clues = {
            "PYTHON": "Programming language used to create this puzzle",
            "PUZZLE": "A game, toy, or problem designed to test ingenuity or knowledge",
            "ALGORITHM": "A step-by-step procedure for solving a problem",
            "GENERATOR": "Device or program that produces something",
            "CROSSWORD": "Word puzzle that takes the form of a grid of squares",
            "CODE": "Instructions written for a computer",
            "PROGRAMMING": "Process of creating computer software",
            "SOFTWARE": "Programs and data that tell a computer how to work",
            "DEVELOPER": "Person who writes computer programs",
            "COMPUTER": "Electronic device for storing and processing data",
            "WEB": "The internet",
            "APP": "Software application",
            "GAME": "Activity for entertainment",
            "DATA": "Information",
            "USER": "Person who uses a program",
            "FILE": "Collection of data stored together",
            "NET": "Network or interconnected system",
            "FORM": "Document with fields to fill in",
            "TEXT": "Written words",
            "EDIT": "To modify or change",
            "SAVE": "To preserve or store",
            "HELP": "Assistance or guidance",
            "TOOL": "Something used to perform a task",
            "BYTE": "Unit of digital information",
            "TYPE": "Category or kind",
            "HOST": "Computer providing services on a network",
            "PORT": "Connection point for computer communication",
            "TIME": "Measured duration",
            "MATH": "Study of numbers and calculations",
            "GRID": "Network of lines forming squares",
            "CELL": "Basic unit in a grid or table",
            "DRAW": "To create a picture",
            "FONT": "Set of characters in a specific style"
        }
        
        if word in sample_clues:
            return sample_clues[word]
        else:
            return f"A {len(word)}-letter word"
    
    def generate_crossword(self, min_words=10, max_attempts=1000):
        """Generate a crossword puzzle"""
        self.create_empty_grid()
        self.debug_info = []
        
        # Check if we have any words
        if not any(self.words_by_length.values()):
            self.debug_info.append("No words available in dictionary")
            return False
        
        # Place the first word in the middle
        available_lengths = sorted([length for length, words in self.words_by_length.items() 
                                  if words and length <= self.size], reverse=True)
        
        if not available_lengths:
            self.debug_info.append("No words of appropriate length found in dictionary")
            return False
            
        word_length = available_lengths[0]
        if not self.words_by_length[word_length]:
            self.debug_info.append(f"No words of length {word_length} available")
            return False
            
        word = random.choice(self.words_by_length[word_length])
        start_col = max(0, min((self.size - word_length) // 2, self.size - word_length))
        start_row = self.size // 2
        
        # Validate positions are within grid
        if start_row < 0 or start_row >= self.size or start_col < 0 or start_col + word_length > self.size:
            self.debug_info.append(f"First word position invalid: row={start_row}, col={start_col}, len={word_length}")
            return False
            
        if not self.place_word(word, start_row, start_col, True, self.generate_clue(word)):
            self.debug_info.append(f"Failed to place first word: {word}")
            return False
            
        # Try to place more words
        attempts = 0
        used_words = {word}
        fallback_used = False
        
        while len(self.word_list) < min_words and attempts < max_attempts:
            attempts += 1
            
            # Choose a random word from current words to intersect with
            if not self.word_list:
                self.debug_info.append("No words in word list to build from")
                break
                
            ref_word, ref_row, ref_col, ref_horizontal = random.choice(self.word_list)
            
            # Choose a random position in the reference word
            ref_pos = random.randint(0, len(ref_word) - 1)
            letter = ref_word[ref_pos]
            
            # Calculate the position in the grid
            if ref_horizontal:
                pos_row, pos_col = ref_row, ref_col + ref_pos
            else:
                pos_row, pos_col = ref_row + ref_pos, ref_col
            
            # Try to place a new word through this position
            direction = not ref_horizontal  # Perpendicular to reference word
            
            # Get words containing the intersection letter
            potential_words = []
            for length, words in self.words_by_length.items():
                if length <= 2:  # Skip very short words
                    continue
                    
                # Skip if word would go out of bounds
                max_extension = length - 1  # Maximum cells the word extends from intersection
                if direction and (pos_row - max_extension < 0 or pos_row + max_extension >= self.size):
                    continue
                if not direction and (pos_col - max_extension < 0 or pos_col + max_extension >= self.size):
                    continue
                    
                for word in words:
                    if word in used_words:
                        continue
                        
                    # Find all positions where this letter appears in the word
                    positions = [i for i, char in enumerate(word) if char == letter]
                    for intersection_pos in positions:
                        potential_words.append((word, intersection_pos))
            
            if not potential_words and not fallback_used and attempts > max_attempts // 2:
                # Fallback: add a word that doesn't intersect with any existing word
                fallback_used = True
                self.debug_info.append("Using fallback word placement")
                
                # Find an empty area in the grid
                for r in range(self.size):
                    for c in range(self.size):
                        # Try to place a horizontal word
                        for length, words in self.words_by_length.items():
                            if length <= 3 or c + length > self.size:
                                continue
                                
                            word_candidates = [w for w in words if w not in used_words]
                            if not word_candidates:
                                continue
                                
                            word = random.choice(word_candidates)
                            if self.can_place_word(word, r, c, True):
                                if self.place_word(word, r, c, True, self.generate_clue(word)):
                                    used_words.add(word)
                                    break
                        
                        # Try to place a vertical word
                        for length, words in self.words_by_length.items():
                            if length <= 3 or r + length > self.size:
                                continue
                                
                            word_candidates = [w for w in words if w not in used_words]
                            if not word_candidates:
                                continue
                                
                            word = random.choice(word_candidates)
                            if self.can_place_word(word, r, c, False):
                                if self.place_word(word, r, c, False, self.generate_clue(word)):
                                    used_words.add(word)
                                    break
            
            if not potential_words:
                continue
                
            random.shuffle(potential_words)
            
            placed = False
            for word, intersection_pos in potential_words:
                try:
                    if direction:  # Vertical
                        start_row = pos_row - intersection_pos
                        if start_row < 0 or start_row + len(word) > self.size:
                            continue
                        if self.can_place_word(word, start_row, pos_col, False):
                            if self.place_word(word, start_row, pos_col, False, self.generate_clue(word)):
                                used_words.add(word)
                                placed = True
                                break
                    else:  # Horizontal
                        start_col = pos_col - intersection_pos
                        if start_col < 0 or start_col + len(word) > self.size:
                            continue
                        if self.can_place_word(word, pos_row, start_col, True):
                            if self.place_word(word, pos_row, start_col, True, self.generate_clue(word)):
                                used_words.add(word)
                                placed = True
                                break
                except Exception as e:
                    self.debug_info.append(f"Error trying to place word {word}: {str(e)}")
        
        self.debug_info.append(f"Generation completed with {len(self.word_list)} words after {attempts} attempts")
        return len(self.word_list) > 0
    
    def get_numbered_grid(self):
        """Get the grid with numbers for the clues"""
        numbered_grid = [row[:] for row in self.grid]
        number_positions = {}
        
        # Sort words to ensure consistent numbering
        sorted_words = sorted(self.word_list, key=lambda w: (w[1], w[2]))
        
        current_number = 1
        for word, row, col, horizontal in sorted_words:
            if (row, col) not in number_positions:
                number_positions[(row, col)] = current_number
                current_number += 1
        
        return numbered_grid, number_positions
    
    def get_clues_list(self):
        """Get formatted lists of across and down clues"""
        across_clues = []
        down_clues = []
        
        # Sort words to ensure consistent numbering
        sorted_words = sorted(self.word_list, key=lambda w: (w[1], w[2]))
        
        number_positions = {}
        current_number = 1
        
        for word, row, col, horizontal in sorted_words:
            if (row, col) not in number_positions:
                number_positions[(row, col)] = current_number
                current_number += 1
                
            clue_num = number_positions[(row, col)]
            clue_text = self.clues.get(word, self.generate_clue(word))
            
            if horizontal:
                across_clues.append((clue_num, clue_text, word))  # Added the word for answer checking
            else:
                down_clues.append((clue_num, clue_text, word))  # Added the word for answer checking
        
        return sorted(across_clues), sorted(down_clues)
    
    def get_cells_with_letters(self):
        """Get a list of all cells that should contain letters"""
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != ' ':
                    cells.append((r, c))
        return cells


class CrosswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Puzzle Generator")
        self.root.geometry("1000x700")
        
        self.generator = CrosswordGenerator()
        self.cell_entries = {}  # Store references to entry widgets
        self.solution_grid = None  # Store the solution
        
        # Set up the UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = Frame(main_frame, padx=5, pady=5)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Grid size selection
        Label(control_frame, text="Grid Size:").pack(side=tk.LEFT, padx=5)
        self.size_var = StringVar(value="15")
        size_entry = Entry(control_frame, textvariable=self.size_var, width=5)
        size_entry.pack(side=tk.LEFT, padx=5)
        
        # Minimum words
        Label(control_frame, text="Min Words:").pack(side=tk.LEFT, padx=5)
        self.min_words_var = StringVar(value="8")
        min_words_entry = Entry(control_frame, textvariable=self.min_words_var, width=5)
        min_words_entry.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        generate_btn = Button(control_frame, text="Generate Puzzle", command=self.generate_crossword)
        generate_btn.pack(side=tk.LEFT, padx=20)
        
        # Check answers button
        check_btn = Button(control_frame, text="Check Answers", command=self.check_answers)
        check_btn.pack(side=tk.LEFT, padx=5)
        
        # Show solution button
        solution_btn = Button(control_frame, text="Show Solution", command=self.show_solution)
        solution_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = Button(control_frame, text="Export Puzzle", command=self.export_puzzle)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Content area - split view
        content_frame = Frame(main_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Crossword grid
        self.grid_frame = Frame(content_frame, bd=2, relief=tk.SUNKEN)
        self.grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Placeholder for grid
        self.grid_placeholder = Label(self.grid_frame, text="Generate a crossword to see it here", height=15)
        self.grid_placeholder.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Clues
        clues_frame = Frame(content_frame, bd=2, relief=tk.SUNKEN, width=400)
        clues_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), 
                         ipadx=10, ipady=10)
        
        # Clues notebook with tabs for Across and Down
        self.clues_notebook = tk.Frame(clues_frame)
        self.clues_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs for the notebook
        tabs_frame = Frame(self.clues_notebook)
        tabs_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.across_tab = Button(tabs_frame, text="Across", 
                               command=lambda: self.show_tab("across"),
                               relief=tk.RAISED, bd=2)
        self.across_tab.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.down_tab = Button(tabs_frame, text="Down", 
                             command=lambda: self.show_tab("down"),
                             relief=tk.FLAT, bd=2)
        self.down_tab.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Content area for the tabs
        self.tab_content = Frame(self.clues_notebook)
        self.tab_content.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # Scrollable clues for each tab
        self.across_clues_text = scrolledtext.ScrolledText(self.tab_content, wrap=tk.WORD)
        self.across_clues_text.pack(fill=tk.BOTH, expand=True)
        
        self.down_clues_text = scrolledtext.ScrolledText(self.tab_content, wrap=tk.WORD)
        
        # Status bar
        self.status_var = StringVar(value="Ready")
        status_bar = Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Default show across clues
        self.current_tab = "across"
    
    def show_tab(self, tab_name):
        """Switch between tabs"""
        if tab_name == "across":
            self.across_tab.config(relief=tk.RAISED)
            self.down_tab.config(relief=tk.FLAT)
            self.down_clues_text.pack_forget()
            self.across_clues_text.pack(fill=tk.BOTH, expand=True)
        else:  # down
            self.across_tab.config(relief=tk.FLAT)
            self.down_tab.config(relief=tk.RAISED)
            self.across_clues_text.pack_forget()
            self.down_clues_text.pack(fill=tk.BOTH, expand=True)
        
        self.current_tab = tab_name
    
    def generate_crossword(self):
        try:
            # Update status
            self.status_var.set("Generating crossword...")
            self.root.update_idletasks()
            
            # Clear previous content
            for widget in self.grid_frame.winfo_children():
                widget.destroy()
                
            self.across_clues_text.delete(1.0, tk.END)
            self.down_clues_text.delete(1.0, tk.END)
            self.cell_entries = {}
                
            # Get parameters
            try:
                grid_size = int(self.size_var.get())
                min_words = int(self.min_words_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Grid size and min words must be integers")
                self.status_var.set("Ready")
                return
                
            # Limit values
            grid_size = max(10, min(grid_size, 25))
            min_words = max(5, min(min_words, 30))
            
            # Generate crossword
            self.generator.set_size(grid_size)
            start_time = time.time()
            
            try:
                success = self.generator.generate_crossword(min_words=min_words)
            except Exception as e:
                self.status_var.set("Error during generation")
                error_msg = f"Generation error: {str(e)}\n\n"
                error_msg += traceback.format_exc()
                self.show_error_dialog("Generation Error", error_msg)
                return
                
            end_time = time.time()
            
            if not success or len(self.generator.word_list) < 1:
                self.status_var.set("Generation failed")
                debug_info = "\n".join(self.generator.debug_info)
                messagebox.showinfo("Generation Failed", 
                                   f"Could not generate a crossword with the specified parameters. Try different settings.\n\nDebug info:\n{debug_info}")
                return
                
            # Save the solution grid
            self.solution_grid = [row[:] for row in self.generator.grid]
            
            # Display the interactive grid
            try:
                grid, number_positions = self.generator.get_numbered_grid()
                cells_with_letters = self.generator.get_cells_with_letters()
                
                # Calculate optimal cell size based on grid size
                cell_size = min(30, 500 // grid_size)
                grid_frame_width = (cell_size + 1) * grid_size + 2
                grid_frame_height = (cell_size + 1) * grid_size + 2
                
                # Create a frame for the grid
                grid_canvas_frame = Frame(self.grid_frame, bd=2, relief=tk.SUNKEN)
                grid_canvas_frame.pack(pady=10, padx=10)
                
                # Create a canvas for the interactive grid
                grid_canvas = tk.Canvas(grid_canvas_frame, width=grid_frame_width, 
                                       height=grid_frame_height, bg="white")
                grid_canvas.pack()
                
                # Create the crossword layout
                for r in range(grid_size):
                    for c in range(grid_size):
                        # Skip cells that don't need to be drawn
                        if (r, c) not in cells_with_letters:
                            continue
                            
                        # Create the cell
                        x1 = c * (cell_size + 1) + 1
                        y1 = r * (cell_size + 1) + 1
                        x2 = x1 + cell_size
                        y2 = y1 + cell_size
                        
                        grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                        
                        # Add number if needed
                        if (r, c) in number_positions:
                            grid_canvas.create_text(x1 + 3, y1 + 3,
                                                  text=str(number_positions[(r, c)]),
                                                  font=("Arial", max(6, cell_size // 4)),
                                                  anchor=tk.NW)
                        
                        # Add an entry widget for user input
                        entry_var = StringVar()
                        entry = Entry(grid_canvas, width=1, font=("Arial", max(10, cell_size // 2)),
                                    justify="center", bd=0, highlightthickness=0, textvariable=entry_var)
                        
                        # Limit entry to one uppercase letter
                        vcmd = (self.root.register(self.validate_entry), '%P')
                        entry.config(validate="key", validatecommand=vcmd)
                        
                        # Position the entry widget in the cell
                        entry_window = grid_canvas.create_window(x1 + cell_size//2, y1 + cell_size//2, 
                                                               window=entry, width=cell_size - 2, 
                                                               height=cell_size - 2)
                        
                        # Store reference to the entry widget
                        self.cell_entries[(r, c)] = (entry, entry_var)
                
                # Display clues
                across_clues, down_clues = self.generator.get_clues_list()
                
                # Display across clues
                self.across_clues_text.insert(tk.END, "ACROSS\n\n")
                for num, clue, word in across_clues:
                    self.across_clues_text.insert(tk.END, f"{num}. {clue}\n\n")
                
                # Display down clues
                self.down_clues_text.insert(tk.END, "DOWN\n\n")
                for num, clue, word in down_clues:
                    self.down_clues_text.insert(tk.END, f"{num}. {clue}\n\n")
                
                self.status_var.set(f"Puzzle generated with {len(self.generator.word_list)} words")
                
                # Show across tab by default
                self.show_tab("across")
                
            except Exception as e:
                self.status_var.set("Error displaying crossword")
                error_msg = f"Display error: {str(e)}\n\n"
                error_msg += traceback.format_exc()
                self.show_error_dialog("Display Error", error_msg)
                
        except Exception as e:
            self.status_var.set("Error")
            error_msg = f"An unexpected error occurred: {str(e)}\n\n"
            error_msg += traceback.format_exc()
            self.show_error_dialog("Error", error_msg)
    
    def validate_entry(self, value):
        """Validate user input to ensure it's a single uppercase letter"""
        if len(value) > 1:
            return False
        if len(value) == 1 and not value.isalpha():
            return False
        return True
    
    def check_answers(self):
        """Check the user's answers against the solution"""
        if not self.solution_grid:
            messagebox.showinfo("No Puzzle", "Generate a puzzle first!")
            return
            
        correct = 0
        total = 0
        
        for (r, c), (entry, var) in self.cell_entries.items():
            total += 1
            user_answer = var.get().upper()
            correct_answer = self.solution_grid[r][c]
            
            if user_answer == correct_answer:
                correct += 1
                entry.config(fg="green")
            else:
                entry.config(fg="red")
        
        accuracy = correct / total * 100 if total > 0 else 0
        messagebox.showinfo("Results", f"You got {correct} out of {total} letters correct! ({accuracy:.1f}%)")
    
    def show_solution(self):
        """Reveal the solution in the grid"""
        if not self.solution_grid:
            messagebox.showinfo("No Puzzle", "Generate a puzzle first!")
            return
            
        for (r, c), (entry, var) in self.cell_entries.items():
            var.set(self.solution_grid[r][c])
            entry.config(fg="blue")
    
    def export_puzzle(self):
        """Export the puzzle to a file"""
        try:
            if not hasattr(self.generator, 'grid') or not self.generator.grid:
                messagebox.showinfo("Export Failed", "Generate a crossword first!")
                return
                
            # Export to a text file
            filename = "crossword_puzzle.txt"
            with open(filename, 'w') as f:
                # Write header
                f.write("CROSSWORD PUZZLE\n\n")
                
                # Get data
                grid, number_positions = self.generator.get_numbered_grid()
                across_clues, down_clues = self.generator.get_clues_list()
                cells_with_letters = self.generator.get_cells_with_letters()
                
                # Write the blank grid (just with numbers)
                f.write("GRID:\n")
                for r in range(self.generator.size):
                    line = ""
                    for c in range(self.generator.size):
                        if (r, c) not in cells_with_letters:
                            line += "  "
                        elif (r, c) in number_positions:
                            line += str(number_positions[(r, c)]).ljust(2)
                        else:
                            line += "_ "
                    f.write(line + "\n")
                f.write("\n")
                
                # Write the clues
                f.write("ACROSS:\n")
                for num, clue, word in across_clues:
                    f.write(f"{num}. {clue}\n")
                f.write("\n")
                    
                f.write("DOWN:\n")
                for num, clue, word in down_clues:
                    f.write(f"{num}. {clue}\n")
                f.write("\n")
                
                # Write solution
                f.write("\nSOLUTION:\n")
                for r in range(self.generator.size):
                    line = ""
                    for c in range(self.generator.size):
                        if (r, c) in cells_with_letters:
                            line += self.solution_grid[r][c] + " "
                        else:
                            line += "  "
                    f.write(line + "\n")
                    
            messagebox.showinfo("Export Successful", f"Puzzle exported to {filename}")
            
        except Exception as e:
            error_msg = f"Export error: {str(e)}\n\n"
            error_msg += traceback.format_exc()
            self.show_error_dialog("Export Error", error_msg)
    
    def show_error_dialog(self, title, error_message):
        """Display an error dialog with details"""
        error_window = tk.Toplevel(self.root)
        error_window.title(title)
        error_window.geometry("600x400")
        
        error_text = scrolledtext.ScrolledText(error_window, wrap=tk.WORD)
        error_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        error_text.insert(tk.END, error_message)
        error_text.config(state=tk.DISABLED)
    
    # ... existing code ...

# Add at the end of the file:
if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordApp(root)
    root.mainloop()