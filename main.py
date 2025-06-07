import tkinter as tk
from ui import GameOfLifeApp

# Entry point of the application
def main():
    root = tk.Tk()
    root.withdraw() # Hide main window until size is chosen

    # Dialog to select grid size
    size_dialog = tk.Toplevel()
    size_dialog.title("Field Size")
    tk.Label(size_dialog, text="Rows:").grid(row=0, column=0)
    tk.Label(size_dialog, text="Columns:").grid(row=1, column=0)

    rows_var = tk.IntVar(value=20)
    cols_var = tk.IntVar(value=20)

    tk.Entry(size_dialog, textvariable=rows_var).grid(row=0, column=1)
    tk.Entry(size_dialog, textvariable=cols_var).grid(row=1, column=1)

    # Start the game after size is chosen
    def confirm():
        size_dialog.destroy()
        root.deiconify()
        root.title("Game of Life - Conway")
        app = GameOfLifeApp(root, rows_var.get(), cols_var.get())
        root.mainloop()

    tk.Button(size_dialog, text="Start", command=confirm).grid(row=2, column=0, columnspan=2, pady=10)

    root.wait_window(size_dialog)


if __name__ == '__main__':
    main()
