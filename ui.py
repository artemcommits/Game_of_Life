import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser, messagebox
from core import GameGrid, PATTERNS

# GUI for Conway's Game of Life
class GameOfLifeApp:
    def __init__(self, master, rows, cols):
        # Initialize main variables
        self.master = master
        self.grid = GameGrid(rows, cols)
        self.cell_size = 20
        self.running = False
        self.alive_color = "#000000"

        # Canvas for displaying cells
        self.canvas = tk.Canvas(master, width=cols*self.cell_size, height=rows*self.cell_size, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # Keyboard shortcuts
        self.master.bind("<space>", lambda e: self.toggle_run())
        self.master.bind("<Return>", lambda e: self.step())
        self.master.bind("<Control-c>", lambda e: self.clear())
        self.master.bind("<Control-s>", lambda e: self.save())
        self.master.bind("<Control-l>", lambda e: self.load())

        # Initialize cell rectangles
        self.rects = [[None for _ in range(cols)] for _ in range(rows)]
        self.draw_grid()

        # Buttons panel
        frame = tk.Frame(master)
        frame.pack()

        tk.Button(frame, text="Start", command=self.start).pack(side=tk.LEFT)
        tk.Button(frame, text="Stop", command=self.stop).pack(side=tk.LEFT)
        tk.Button(frame, text="Next", command=self.step).pack(side=tk.LEFT)
        tk.Button(frame, text="Clear", command=self.clear).pack(side=tk.LEFT)
        tk.Button(frame, text="Set Rules", command=self.set_rules).pack(side=tk.LEFT)
        tk.Button(frame, text="Save", command=self.save).pack(side=tk.LEFT)
        tk.Button(frame, text="Load", command=self.load).pack(side=tk.LEFT)
        tk.Button(frame, text="Load Pattern", command=self.load_pattern_dialog).pack(side=tk.LEFT)
        tk.Button(frame, text="Color", command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(frame, text="Resize", command=self.resize_grid).pack(side=tk.LEFT)
        tk.Button(frame, text="Controls", command=self.show_controls).pack(side=tk.LEFT)

    # Draw initial empty grid
    def draw_grid(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                fill = self.alive_color if self.grid.grid[i][j] else "white"
                self.rects[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    # Redraw grid based on current state
    def redraw(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = self.alive_color if self.grid.grid[i][j] else "white"
                self.canvas.itemconfig(self.rects[i][j], fill=color)

    # Update game one step forward
    def update(self):
        self.grid.update()
        self.redraw()

    # Start continuous simulation
    def start(self):
        self.running = True
        self.run()

    # Stop simulation
    def stop(self):
        self.running = False

    # Run loop with delay
    def run(self):
        if self.running:
            self.update()
            self.master.after(200, self.run)

    # Toggle simulation on/off
    def toggle_run(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # Single step forward
    def step(self):
        self.update()

    # Clear grid
    def clear(self):
        self.running = False
        self.grid.clear()
        self.redraw()

    # Toggle a cell on mouse click
    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            self.grid.toggle(row, col)
            self.redraw()

    # Set custom survival/birth rules
    def set_rules(self):
        rule_str = simpledialog.askstring("Rules", "Enter rules in format S/B (e.g., 23/3):")
        if rule_str and '/' in rule_str:
            survive, birth = rule_str.split('/')
            self.grid.survive_rules = {int(ch) for ch in survive if ch.isdigit()}
            self.grid.birth_rules = {int(ch) for ch in birth if ch.isdigit()}

    # Save current grid to file
    def save(self):
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            self.grid.save_to_file(file)

    # Load grid from file
    def load(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            self.grid.load_from_file(file)
            self.redraw()

    # Dialog to load a predefined pattern
    def load_pattern_dialog(self):
        win = tk.Toplevel(self.master)
        win.title("Choose Pattern")
        tk.Label(win, text="Choose a pattern:").pack(pady=10)
        for name in PATTERNS:
            tk.Button(win, text=name.title(), command=lambda n=name: self.load_pattern(PATTERNS[n], win)).pack(pady=5)

    # Place selected pattern in the center
    def load_pattern(self, pattern, window=None):
        self.clear()
        self.grid.place_pattern(pattern)
        self.redraw()
        if window:
            window.destroy()

    # Change the color of alive cells
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Cell Color")
        if color[1]:
            self.alive_color = color[1]
            self.redraw()

    # Resize the game grid
    def resize_grid(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Resize Grid")

        tk.Label(dialog, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(dialog, text="Columns:").grid(row=1, column=0, padx=5, pady=5)

        rows_var = tk.IntVar(value=self.grid.rows)
        cols_var = tk.IntVar(value=self.grid.cols)

        tk.Entry(dialog, textvariable=rows_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(dialog, textvariable=cols_var).grid(row=1, column=1, padx=5, pady=5)

        def apply_resize():
            new_rows = rows_var.get()
            new_cols = cols_var.get()
            if new_rows > 0 and new_cols > 0:
                self.grid = GameGrid(new_rows, new_cols)
                self.canvas.config(width=new_cols * self.cell_size, height=new_rows * self.cell_size)
                self.rects = [[None for _ in range(new_cols)] for _ in range(new_rows)]
                self.canvas.delete("all")
                self.draw_grid()
                dialog.destroy()

        tk.Button(dialog, text="Apply", command=apply_resize).grid(row=2, column=0, columnspan=2, pady=10)

    # Show keyboard control instructions
    def show_controls(self):
        msg = (
            "Space: Start/Stop\n"
            "Enter: Next Step\n"
            "Ctrl+C: Clear\n"
            "Ctrl+S: Save\n"
            "Ctrl+L: Load\n"
            "Mouse Click: Toggle Cell"
        )
        messagebox.showinfo("Controls", msg)
