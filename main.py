import tkinter as tk
from ui import GameOfLifeApp


def main():
    """
    Launches the Game of Life application.

    Opens a dialog to select the initial grid size,
    then starts the main application window.
    """
    root = tk.Tk()
    root.withdraw()

    size_dialog = tk.Toplevel()
    size_dialog.title("Field Size")
    tk.Label(size_dialog, text="Rows:").grid(row=0, column=0)
    tk.Label(size_dialog, text="Columns:").grid(row=1, column=0)

    rows_var = tk.IntVar(value=20)
    cols_var = tk.IntVar(value=20)

    tk.Entry(size_dialog, textvariable=rows_var).grid(row=0, column=1)
    tk.Entry(size_dialog, textvariable=cols_var).grid(row=1, column=1)

    def confirm():
        """
        Confirms the size input and launches the Game of Life UI.
        """
        size_dialog.destroy()
        root.deiconify()
        root.title("Game of Life - Conway")
        app = GameOfLifeApp(root, rows_var.get(), cols_var.get())
        root.mainloop()

    tk.Button(size_dialog, text="Start", command=confirm).grid(row=2, column=0, columnspan=2, pady=10)

    root.wait_window(size_dialog)


if __name__ == '__main__':
    main()
