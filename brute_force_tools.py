# _______________This file includes some useful functions for the brute force algorithm_______________ # 
from array import * 
from collections import defaultdict 
from checking_functions import * 
from logic import * 


# _____ The specific function finds the empty cell with the least number of possible values____ #
def fewest_possible_values(sudoku_array, sudoku_possibles): 
    """
    Finds the empty cell with the fewest possible values and returns its index.
    This is useful for the brute force algorithm to minimize the branching factor.
    """
    global cell 
    minimum = 10  # Initialize minimum with a value larger than any possible number of candidates
    for r in range(9): 
        for c in range(9): 
            i = r * 9 + c 
            if sudoku_array[i] == 0 and len(sudoku_possibles[i]) < minimum:  
                minimum = len(sudoku_possibles[i])  # Update the minimum possible values
                cell = i  # Store the index of the cell with the fewest values
    return cell


# _____ This function returns a list with all empty cells in the grid____ #
def empty_function(sudoku_array): 
    """
    Returns a list of all empty cells (cells with a value of 0) in the Sudoku grid.
    This is used to identify the locations that need to be filled.
    """
    empty = [] 
    for r in range(9): 
        for c in range(9): 
            i = r * 9 + c 
            if sudoku_array[i] == 0:  # If the cell is empty, add it to the list
                empty.append(i)             
    return empty


# _____ For every zero cell, it finds its possible values and returns a list of lists____ #
def valid_values(sudoku_array, sudoku_possibles): 
    """
    For every empty cell in the Sudoku grid, finds the possible valid values.
    Returns a list of lists where each sublist contains the possible values for a specific cell.
    """
    empty = empty_function(sudoku_array)  # Get all empty cells
    k = len(empty)  # Number of empty cells
    valid = [[] for _ in range(k)]  # Initialize a list of lists to store possible values
    l = 0  # Counter for empty cells

    # Loop through the grid and populate the valid values for each empty cell
    for r in range(9): 
        for c in range(9): 
            i = r * 9 + c 
            if sudoku_array[i] == 0:  # If the cell is empty
                for j in sudoku_possibles[i]: 
                    valid[l].append(j)  # Add possible values to the sublist
                l += 1        
    return valid
