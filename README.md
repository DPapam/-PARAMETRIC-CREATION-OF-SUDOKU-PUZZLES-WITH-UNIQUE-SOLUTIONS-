# -PARAMETRIC-CREATION-OF-SUDOKU-PUZZLES-WITH-UNIQUE-SOLUTIONS-

To run this program you have to:

-> Step 1:  Download (if you don't already have) the necessary libraries:
- pygame (pip install pygame), this library helps with the creation of the user interface
- itertools
- random
- time

-> Step 2:  Make sure to have the pictures folder and the Mirage.wav in the directory of the .py files

-> Step 3:  Run the modified_graphics.py file which has the graphics of the program

-> Step 4:  Solve some Sudoku puzzles :)


Explanation of each .py file:

- modified_graphics.py:  Contains functions to display the puzzle and its elements.
- generation.py:  Handles the generation of Sudoku puzzles.
- logic.py:  Implements the core logic-solving techniques for Sudoku, applying various strategies to fill in the puzzle.
- single_solution.py:  Ensures that the generated Sudoku puzzle has only one valid solution.
- sudoku_generator.py:  Generates Sudoku grids with a specified number of empty cells, based on difficulty.
- empty_cells.py:  Determines and manages the number of empty cells in a generated Sudoku puzzle, contributing to difficulty.
- brute_force_tools.py:  It has functions that are useful for the brute-force technique.
- checking_functions.py:  Contains utility functions for checking Sudoku grid states, validating solutions, and detecting errors.
