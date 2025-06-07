import json
import os

# Handles the logic and state of the game grid
class GameGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.survive_rules = {2, 3}
        self.birth_rules = {3}

    # Set all cells to dead
    def clear(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    # Toggle the state of a single cell
    def toggle(self, row, col):
        self.grid[row][col] ^= 1
    # Compute the next generation
    def update(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] and neighbors in self.survive_rules:
                    new_grid[i][j] = 1
                elif not self.grid[i][j] and neighbors in self.birth_rules:
                    new_grid[i][j] = 1
        self.grid = new_grid

    # Count alive neighbors with wrapping
    def count_neighbors(self, row, col):
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        count = 0
        for dr, dc in directions:
            r, c = (row + dr) % self.rows, (col + dc) % self.cols
            count += self.grid[r][c]
        return count
    # Save grid to a JSON file
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.grid, f)
    # Load grid from a JSON file
    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.grid = json.load(f)

    # Place a pattern in the center of the grid
    def place_pattern(self, pattern):
        start_row = (self.rows - len(pattern)) // 2
        start_col = (self.cols - len(pattern[0])) // 2
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                if 0 <= start_row + i < self.rows and 0 <= start_col + j < self.cols:
                    self.grid[start_row + i][start_col + j] = pattern[i][j]

# Predefined patterns for the game
PATTERNS = {
    "glider": [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "pulsar": [
        [0,0,1,1,1,0,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,1,0,1,0,0,0,0,1],
        [1,0,0,0,0,1,0,1,0,0,0,0,1],
        [1,0,0,0,0,1,0,1,0,0,0,0,1],
        [0,0,1,1,1,0,0,0,1,1,1,0,0],
    ],
    "lightweight spaceship": [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
    ]
}
