import random

class SudokuGenerator:
    """
    This class generates a complete Sudoku board and solves it using backtracking.
    It also validates the board configuration and checks if numbers can be placed in specific positions.
    """

    def __init__(self):
        """
        Initializes the Sudoku board and prepares the necessary arrays to store the grid.
        The Sudoku grid is generated in a fully solved state.
        """
        self.board = [[0] * 9 for _ in range(9)]  # Initialize the 9x9 board with zeros
        self.sudoku_possible = [[None] for _ in range(81)]  # Possible values for each cell
        self.sudoku_array = [0] * 81  # Store the Sudoku board in a 1D array
        self.generate_full_board()  # Generate a fully solved Sudoku board


    # Generates a full Sudoku board using backtracking
    def generate_full_board(self):
        """
        Generates a fully solved Sudoku board using the backtracking algorithm.
        After solving the board, stores the values in the sudoku_array and sudoku_possible lists.
        """
        self.solve_board(self.board)  # Solve the board using backtracking
        for r in range(9):
            for c in range(9):
                self.sudoku_array[r * 9 + c] = self.board[r][c]  # Flatten the 2D board into a 1D array
        self.sudoku_possible = [[self.sudoku_array[i]] for i in range(81)]  # Set possible values for each cell


    # Solve the board using backtracking
    def solve_board(self, board):
        """
        Solves the Sudoku board using a backtracking algorithm.
        This method recursively attempts to place numbers in empty cells and backtracks when necessary.
        Returns True when the board is completely solved.
        """
        empty = self.find_empty(board)  # Find the next empty cell
        if not empty:
            return True  # Board is completely solved if no empty cells are found
        row, col = empty
        numbers = list(range(1, 10))  # Generate numbers from 1 to 9
        random.shuffle(numbers)  # Shuffle to ensure randomness in solving
        for num in numbers:
            if self.is_valid(board, num, row, col):  # Check if the number can be placed
                board[row][col] = num
                if self.solve_board(board):  # Recursive call to continue solving
                    return True
                board[row][col] = 0  # Reset the cell if no solution is found
        return False  # Backtrack if no valid number can be placed


    # Find an empty cell
    def find_empty(self, board):
        """
        Finds the next empty cell (represented by a 0) in the Sudoku board.
        Returns the row and column of the empty cell, or None if the board is full.
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:  # Empty cell found
                    return (i, j)
        return None  # No empty cell found, board is full


    # Check if placing a number in a position is valid
    def is_valid(self, board, num, row, col):
        """
        Checks if placing the number 'num' in the position (row, col) is valid.
        The number is valid if it does not appear in the same row, column, or 3x3 sub-grid.
        Returns True if the placement is valid, False otherwise.
        """
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3x3 box
        box_row, box_col = row // 3 * 3, col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:  # Number already exists in the sub-grid
                    return False
        return True  # Placement is valid
