import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser, messagebox
from core import GameGrid, PATTERNS

class GameOfLifeApp:
    """
    GUI application class for Conway's Game of Life.

    :param master: The root Tkinter window.
    :type master: tk.Tk
    :param rows: Initial number of rows for the grid.
    :type rows: int
    :param cols: Initial number of columns for the grid.
    :type cols: int
    """

    def __init__(self, master, rows, cols):
        """
        Initializes the GUI, canvas, controls, and binds events.
        """
        self.master = master
        self.grid = GameGrid(rows, cols)
        self.cell_size = 20
        self.running = False
        self.alive_color = "#000000"

        self.canvas = tk.Canvas(master,
                                width=cols*self.cell_size,
                                height=rows*self.cell_size,
                                bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.master.bind("<space>", lambda e: self.toggle_run())
        self.master.bind("<Return>", lambda e: self.step())
        self.master.bind("<Control-c>", lambda e: self.clear())
        self.master.bind("<Control-s>", lambda e: self.save())
        self.master.bind("<Control-l>", lambda e: self.load())

        self.rects = [[None for _ in range(cols)] for _ in range(rows)]
        self.draw_grid()

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

    def draw_grid(self):
        """
        Draws the grid layout on the canvas.
        """
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                fill = self.alive_color if self.grid.grid[i][j] else "white"
                self.rects[i][j] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill, outline="gray")

    def redraw(self):
        """
        Redraws cells on the canvas to reflect the grid state.
        """
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = self.alive_color if self.grid.grid[i][j] else "white"
                self.canvas.itemconfig(self.rects[i][j], fill=color)

    def update(self):
        """
        Updates the logical grid and redraws the canvas.
        """
        self.grid.update()
        self.redraw()

    def start(self):
        """
        Starts the simulation loop.
        """
        self.running = True
        self.run()

    def stop(self):
        """
        Stops the simulation loop.
        """
        self.running = False

    def run(self):
        """
        Internal loop to repeatedly update and redraw while running.
        """
        if self.running:
            self.update()
            self.master.after(200, self.run)

    def toggle_run(self):
        """
        Toggles between running and stopped simulation.
        """
        if self.running:
            self.stop()
        else:
            self.start()

    def step(self):
        """
        Advances a single generation in the simulation.
        """
        self.update()

    def clear(self):
        """
        Clears the grid and stops the simulation.
        """
        self.running = False
        self.grid.clear()
        self.redraw()

    def on_click(self, event):
        """
        Toggles a cell's alive/dead state on canvas click.

        :param event: The mouse click event.
        :type event: tk.Event
        """
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            self.grid.toggle(row, col)
            self.redraw()

    def set_rules(self):
        """
        Opens a dialog to input new survival/birth rules (format '23/3').
        """
        rule_str = simpledialog.askstring("Rules", "Enter rules in format S/B (e.g., 23/3):")
        if rule_str and '/' in rule_str:
            survive, birth = rule_str.split('/')
            self.grid.survive_rules = {int(ch) for ch in survive if ch.isdigit()}
            self.grid.birth_rules = {int(ch) for ch in birth if ch.isdigit()}

    def save(self):
        """
        Opens a file dialog to save the grid to JSON.
        """
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            self.grid.save_to_file(file)

    def load(self):
        """
        Opens a file dialog to load the grid from JSON.
        """
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            self.grid.load_from_file(file)
            self.redraw()

    def load_pattern_dialog(self):
        """
        Opens a dialog to choose and load a predefined pattern.
        """
        win = tk.Toplevel(self.master)
        win.title("Choose Pattern")
        tk.Label(win, text="Choose a pattern:").pack(pady=10)
        for name in PATTERNS:
            tk.Button(
                win,
                text=name.title(),
                command=lambda n=name: self.load_pattern(PATTERNS[n], win)
            ).pack(pady=5)

    def load_pattern(self, pattern, window=None):
        """
        Places a predefined pattern on the grid.

        :param pattern: 2D pattern list (0 or 1).
        :type pattern: list[list[int]]
        :param window: Optional dialog window to destroy after loading.
        :type window: tk.Toplevel or None
        """
        self.clear()
        self.grid.place_pattern(pattern)
        self.redraw()
        if window:
            window.destroy()

    def choose_color(self):
        """
        Opens a color picker to change the color of live cells.
        """
        color = colorchooser.askcolor(title="Choose Cell Color")
        if color[1]:
            self.alive_color = color[1]
            self.redraw()

    def resize_grid(self):
        """
        Opens a dialog to input new grid size and resizes the grid accordingly.
        """
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
                self.canvas.config(width=new_cols * self.cell_size,
                                   height=new_rows * self.cell_size)
                self.rects = [[None for _ in range(new_cols)]
                              for _ in range(new_rows)]
                self.canvas.delete("all")
                self.draw_grid()
                dialog.destroy()

        tk.Button(dialog, text="Apply", command=apply_resize).grid(
            row=2, column=0, columnspan=2, pady=10)

    def show_controls(self):
        """
        Displays keyboard and mouse controls in an information dialog.
        """
        msg = (
            "Space: Start/Stop\n"
            "Enter: Next Step\n"
            "Ctrl+C: Clear\n"
            "Ctrl+S: Save\n"
            "Ctrl+L: Load\n"
            "Mouse Click: Toggle Cell"
        )
        messagebox.showinfo("Controls", msg)
