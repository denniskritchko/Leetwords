import tkinter as tk
from tkinter import messagebox, scrolledtext, Frame, Label, Button, Entry, StringVar
import traceback
import time
import tkinter.ttk as ttk
from crossword import CrosswordGenerator

class CrosswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Creator")
        
        # Create the crossword generator without dictionary path
        self.generator = CrosswordGenerator()
        
        # Canvas properties
        self.cell_size = 40
        self.canvas_width = 800
        self.canvas_height = 600
        self.offset_x = 0  # Offset for panning
        self.offset_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel (top)
        control_panel = ttk.Frame(main_frame, padding="5")
        control_panel.pack(fill=tk.X)
        
        # Grid size and min words
        settings_frame = ttk.LabelFrame(control_panel, text="Settings", padding="5")
        settings_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(settings_frame, text="Min Words:").pack(side=tk.LEFT, padx=5)
        self.min_words_var = tk.StringVar(value="10")
        min_words_entry = ttk.Entry(settings_frame, textvariable=self.min_words_var, width=5)
        min_words_entry.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(control_panel, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Generate button
        generate_btn = ttk.Button(control_panel, text="Generate Crossword", 
                                command=self.generate_crossword)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_panel, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=5)
        
        # Content area - split view
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Crossword canvas
        canvas_frame = ttk.Frame(content_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, 
                              height=self.canvas_height, bg='white',
                              bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events for panning
        self.canvas.bind('<ButtonPress-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.end_drag)
        
        # Bind mouse wheel for zooming
        self.canvas.bind('<MouseWheel>', self.zoom)
        
        # Right side - Clues
        clues_frame = ttk.Frame(content_frame)
        clues_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Clues notebook
        self.clues_notebook = ttk.Notebook(clues_frame)
        self.clues_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Across clues tab
        across_frame = ttk.Frame(self.clues_notebook)
        self.clues_notebook.add(across_frame, text='Across')
        self.across_clues_text = tk.Text(across_frame, wrap=tk.WORD, width=40)
        across_scrollbar = ttk.Scrollbar(across_frame, command=self.across_clues_text.yview)
        self.across_clues_text.config(yscrollcommand=across_scrollbar.set)
        self.across_clues_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        across_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Down clues tab
        down_frame = ttk.Frame(self.clues_notebook)
        self.clues_notebook.add(down_frame, text='Down')
        self.down_clues_text = tk.Text(down_frame, wrap=tk.WORD, width=40)
        down_scrollbar = ttk.Scrollbar(down_frame, command=self.down_clues_text.yview)
        self.down_clues_text.config(yscrollcommand=down_scrollbar.set)
        self.down_clues_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        down_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_drag(self, event):
        """Start canvas dragging"""
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag(self, event):
        """Handle canvas dragging"""
        if not self.is_dragging:
            return
        
        # Calculate the distance moved
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        # Update the offset
        self.offset_x += dx
        self.offset_y += dy
        
        # Update the drag start position
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        # Redraw the crossword
        self.redraw_crossword()
    
    def end_drag(self, event):
        """End canvas dragging"""
        self.is_dragging = False
    
    def zoom(self, event):
        """Handle zooming"""
        # Zoom in/out based on mouse wheel direction
        if event.delta > 0:
            self.cell_size = min(80, self.cell_size + 5)
        else:
            self.cell_size = max(20, self.cell_size - 5)
        self.redraw_crossword()
    
    def generate_crossword(self):
        """Initialize an empty crossword grid"""
        # Reset the offset to center
        self.offset_x = self.canvas_width // 2
        self.offset_y = self.canvas_height // 2
        
        # Reset puzzle state
        self.generator.create_empty_grid()
        self.selected_cell = None
        self.current_word_cells = []
        
        # Draw the empty grid
        self.redraw_crossword()
    
    def redraw_crossword(self):
        """Redraw the crossword puzzle"""
        self.canvas.delete("all")
        
        if not self.generator.word_list:
            return
        
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
        
        # Draw word numbers
        number = 1
        numbered_cells = set()
        
        # Sort words to ensure consistent numbering
        sorted_words = sorted(self.generator.word_list, 
                            key=lambda x: (x[1], x[2]))  # Sort by row, then col
        
        for word, row, col, _ in sorted_words:
            if (row, col) not in numbered_cells:
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
                self.canvas.create_text(x + 5, y + 5, 
                                      text=str(number), 
                                      font=('Arial', 8),
                                      anchor='nw')
                numbered_cells.add((row, col))
                number += 1
    
    def update_clues(self):
        """Update the clues text widgets"""
        # Clear existing clues
        self.across_clues_text.delete(1.0, tk.END)
        self.down_clues_text.delete(1.0, tk.END)
        
        # Get clues
        across_clues, down_clues = self.generator.get_clues_list()
        
        # Update across clues
        for num, clue, word in across_clues:
            self.across_clues_text.insert(tk.END, f"{num}. {clue}\n\n")
        
        # Update down clues
        for num, clue, word in down_clues:
            self.down_clues_text.insert(tk.END, f"{num}. {clue}\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordApp(root)
    root.mainloop() 