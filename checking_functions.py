#________This file includes the function which checks whether the sudoku has been solved or not_________# 
#____________Checking for zero cells or duplicates________________# 
from array import * 
from collections import defaultdict 


#_________This function checks if each row in the Sudoku grid contains all unique values from 1 to 9_________# 
def row_checking(sudoku_array): 
    """
    Checks whether each row in the Sudoku grid has no duplicates and contains no zero values.
    Returns True if all rows are valid, otherwise False.
    """
    flag_r = True  # Flag to indicate if all rows are valid
    rows_array = [[] for _ in range(9)]  # Create a 2D list to store rows

    for r in range(0, 9):  # Loop through each row
        for c in range(0, 9):  # Loop through each column in the row
            cell = r * 9 + c  # Calculate the cell index
            rows_array[r].append(sudoku_array[cell])  # Add cell value to the row

    for row in rows_array:  # Check each row for duplicates or zeroes
        row_set = set(row)  # Convert the row to a set to remove duplicates
        if str(0) in row_set or len(row_set) != 9:  # Check for zeroes or duplicates
            flag_r = False  # If invalid, set flag to False

    return flag_r  # Return the result of the row check


#_________This function checks if each column in the Sudoku grid contains all unique values from 1 to 9_________# 
def column_checking(sudoku_array): 
    """
    Checks whether each column in the Sudoku grid has no duplicates and contains no zero values.
    Returns True if all columns are valid, otherwise False.
    """
    flag_c = True  # Flag to indicate if all columns are valid
    columns_array = [[] for _ in range(9)]  # Create a 2D list to store columns

    for c in range(0, 9):  # Loop through each column
        for r in range(0, 9):  # Loop through each row in the column
            cell = r * 9 + c  # Calculate the cell index
            columns_array[c].append(sudoku_array[cell])  # Add cell value to the column

    for column in columns_array:  # Check each column for duplicates or zeroes
        column_set = set(column)  # Convert the column to a set to remove duplicates
        if str(0) in column_set or len(column_set) != 9:  # Check for zeroes or duplicates
            flag_c = False  # If invalid, set flag to False

    return flag_c  # Return the result of the column check


#_________This function checks if each 3x3 subgrid in the Sudoku grid contains all unique values from 1 to 9_________# 
def minigrid_checking(sudoku_array): 
    """
    Checks whether each 3x3 subgrid in the Sudoku grid has no duplicates and contains no zero values.
    Returns True if all subgrids are valid, otherwise False.
    """
    flag_m = True  # Flag to indicate if all subgrids are valid
    minigrids_array = [[] for _ in range(9)]  # Create a list for each subgrid
    the_list = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting indices for each 3x3 subgrid
    j = 0  # Subgrid index

    for i in the_list:  # Loop through each subgrid
        start_r = i // 9  # Starting row of the subgrid
        start_c = i % 9  # Starting column of the subgrid
        stop_c = start_c + 3  # Ending column of the subgrid
        stop_r = start_r + 3  # Ending row of the subgrid

        for r in range(start_r, stop_r):  # Loop through the rows of the subgrid
            for c in range(start_c, stop_c):  # Loop through the columns of the subgrid
                cell = r * 9 + c  # Calculate the cell index
                minigrids_array[j].append(sudoku_array[cell])  # Add cell value to the subgrid

        j = j + 1  # Move to the next subgrid

    for minigrid in minigrids_array:  # Check each subgrid for duplicates or zeroes
        minigrid_set = set(minigrid)  # Convert the subgrid to a set to remove duplicates
        if str(0) in minigrid_set or len(minigrid_set) != 9:  # Check for zeroes or duplicates
            flag_m = False  # If invalid, set flag to False

    return flag_m  # Return the result of the subgrid check


#_________This function checks if the Sudoku grid is completely valid by checking rows, columns, and subgrids_________# 
def final_checking(sudoku_array): 
    """
    Performs the final check to ensure the Sudoku grid is fully valid.
    This includes checking all rows, columns, and subgrids for validity.
    Returns True if the entire grid is valid, otherwise False.
    """
    flag_r = row_checking(sudoku_array)  # Check the rows
    flag_c = column_checking(sudoku_array)  # Check the columns
    flag_m = minigrid_checking(sudoku_array)  # Check the subgrids

    if flag_r and flag_c and flag_m:  # If all checks pass, the grid is valid
        flag_1 = True 
    else: 
        flag_1 = False  # If any check fails, the grid is invalid

    return flag_1  # Return the overall result
