import json
import os

class GameGrid:
    """
    Represents the logic grid for Conway's Game of Life.

    :param rows: Number of rows in the grid.
    :type rows: int
    :param cols: Number of columns in the grid.
    :type cols: int
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.survive_rules = {2, 3}
        self.birth_rules = {3}

    def clear(self):
        """
        Clears the grid by setting all cells to dead (0).
        """
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def toggle(self, row, col):
        """
        Toggles the state of a specific cell.

        :param row: Row index of the cell.
        :type row: int
        :param col: Column index of the cell.
        :type col: int
        """
        self.grid[row][col] ^= 1

    def update(self):
        """
        Advances the grid by applying Game of Life rules to each cell.
        """
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] and neighbors in self.survive_rules:
                    new_grid[i][j] = 1
                elif not self.grid[i][j] and neighbors in self.birth_rules:
                    new_grid[i][j] = 1
        self.grid = new_grid

    def count_neighbors(self, row, col):
        """
        Counts alive neighbors for a given cell, wrapping around edges.

        :param row: Row index of the cell.
        :type row: int
        :param col: Column index of the cell.
        :type col: int
        :return: Number of live neighboring cells.
        :rtype: int
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = (row + dr) % self.rows, (col + dc) % self.cols
            count += self.grid[r][c]
        return count

    def save_to_file(self, filename):
        """
        Saves the current grid state to a JSON file.

        :param filename: Path to save the file.
        :type filename: str
        """
        with open(filename, 'w') as f:
            json.dump(self.grid, f)

    def load_from_file(self, filename):
        """
        Loads grid state from a JSON file if it exists.

        :param filename: Path to load the file from.
        :type filename: str
        """
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.grid = json.load(f)

    def place_pattern(self, pattern):
        """
        Places a predefined pattern at the center of the grid.

        :param pattern: 2D list of integers (0 or 1) representing the pattern.
        :type pattern: list[list[int]]
        """
        start_row = (self.rows - len(pattern)) // 2
        start_col = (self.cols - len(pattern[0])) // 2
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                if 0 <= start_row + i < self.rows and 0 <= start_col + j < self.cols:
                    self.grid[start_row + i][start_col + j] = pattern[i][j]


PATTERNS = {
    "glider": [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "pulsar": [
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    ],
    "lightweight spaceship": [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
    ]
}
