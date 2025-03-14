import tkinter as tk
from tkinter import messagebox, scrolledtext, Frame, Label, Button, Entry, StringVar
import traceback
import time
from crossword import CrosswordGenerator

class CrosswordApp:
    def __init__(self, root, dictionary_path='dictionary.txt'):
        self.root = root
        self.root.title("Crossword Puzzle Generator")
        self.root.geometry("1000x700")
        
        self.generator = CrosswordGenerator(dictionary_path)
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
    
    def validate_entry(self, value):
        """Validate user input to ensure it's a single uppercase letter"""
        if len(value) > 1:
            return False
        if len(value) == 1 and not value.isalpha():
            return False
        return True
    
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordApp(root)
    root.mainloop() 