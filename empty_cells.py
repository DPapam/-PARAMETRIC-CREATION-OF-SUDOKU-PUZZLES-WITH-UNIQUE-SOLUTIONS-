# ____________This file includes essential functions for vacating cells procedure ____________ #
from array import * 
from collections import defaultdict 
import random 

backup_actual_stack = [] 
backup_possible_stack = [] 


# __The role of this function is to vacate "number" cells, on condition that there are at least "givens" completed cells in each row and column__ #
def empty_cells(number, givens, sudoku_array, sudoku_possible, first_sudoku, first_possible): 
    """
    Vacates a given number of cells in the Sudoku grid while ensuring that there are at least
    'givens' completed cells in each row and column.
    """
    count_rows = [9] * 9  # Number of confirmed cells in each row
    count_columns = [9] * 9  # Number of confirmed cells in each column
    
    for i in range(number): 
        # Call the check function until a non-zero cell, which can be vacated, is found              
        row, column, sudoku_array, sudoku_possible, count_rows, count_columns, flag_2 = check(givens, sudoku_array, sudoku_possible, first_sudoku, first_possible, count_rows, count_columns) 
 
        while not flag_2: 
            row, column, sudoku_array, sudoku_possible, count_rows, count_columns, flag_2 = check(givens, sudoku_array, sudoku_possible, first_sudoku, first_possible, count_rows, count_columns)  
       
        count_rows[row] -= 1 
        count_columns[column] -= 1  # Update row and column counts
        cell = row * 9 + column 
        sudoku_array[cell] = 0  # Vacate the specific cell
        sudoku_possible[cell] = [] 
        for j in range(1, 10): 
            sudoku_possible[cell].append(j)  # Add back possible values to the vacated cell   
    return sudoku_array, sudoku_possible, count_rows, count_columns


# ____________This function determines the location of empty cells___________ #
def check(givens, array, possible, first_sudoku, first_possible, count_rows, count_columns): 
    """
    Determines which cells in the Sudoku grid can be vacated based on the number of 'givens'
    and checks the row and column counts to find appropriate cells.
    """
    rowlist = [] 
    collist = [] 
    rowlist.clear 
    collist.clear 
    flag_1 = True 
    flag_2 = True 
    counter = 0 

    # Identify rows and columns with more than the minimum 'givens'
    for i in range(9): 
        if count_rows[i] > givens: 
            rowlist.append(i) 
        if count_columns[i] > givens: 
            collist.append(i) 
    
    for i in rowlist: 
        for j in collist: 
            x = i * 9 + j  # Check possible combinations
            if array[x] != 0: 
                counter += 1 
                flag_1 = False 
                break 
        if not flag_1:
            break

    row, column = choice(count_rows, count_columns, givens)    
    cell = row * 9 + column  # Select a cell to vacate

    # Ensure the selected cell is non-zero before vacating
    while array[cell] == 0: 
        if counter != 0:  # Continue searching if there are still cells that can be vacated  
            row, column = choice(count_rows, count_columns, givens) 
            cell = row * 9 + column 
        else: 
            row = random.randrange(0, 9)  # Restore a zero cell to its original value
            column = random.randrange(0, 9) 
            cell_zero = row * 9 + column 
            while array[cell_zero] != 0:  # Find an empty (zero) cell 
                row = random.randrange(0, 9) 
                column = random.randrange(0, 9) 
                cell_zero = row * 9 + column   
            array[cell_zero] = first_sudoku[cell_zero]  # Restore the original value
            possible[cell_zero] = first_possible[cell_zero] 
            count_columns[column] += 1 
            count_rows[row] += 1  # Refresh row and column counts
            flag_2 = False  

            return row, column, array, possible, count_rows, count_columns, flag_2 

    return row, column, array, possible, count_rows, count_columns, flag_2


# ____________This function determines the location of another cell to vacate___________ #
def check_1(givens, array, possible, first_sudoku, first_possible, count_rows, count_columns, cell): 
    """
    Similar to 'check', but ensures that the newly vacated cell is not the same as the previously restored cell.
    It also ensures that at least one cell can be vacated based on the 'givens' requirement.
    """
    rowlist = [] 
    collist = [] 
    rowlist.clear 
    collist.clear 
    flag_1 = True 
    flag_2 = True 
    counter = 0 

    # Identify rows and columns with more than the minimum 'givens'
    for i in range(9): 
        if count_rows[i] > givens: 
            rowlist.append(i) 
        if count_columns[i] > givens: 
            collist.append(i) 
    
    for i in rowlist: 
        for j in collist: 
            x = i * 9 + j  # Check possible combinations
            if array[x] != 0 and x != cell: 
                counter += 1 
                flag_1 = False 
                break 
        if not flag_1:
            break

    row, column = choice(count_rows, count_columns, givens) 
    cell_new = row * 9 + column 

    # Ensure the new cell is non-zero and not the same as the previous cell
    while array[cell_new] == 0 or cell_new == cell: 
        if counter != 0:  # Continue searching for valid cells to vacate 
            row, column = choice(count_rows, count_columns, givens) 
            cell_new = row * 9 + column 
        else: 
            row = random.randrange(0, 9)  # Restore another zero cell
            column = random.randrange(0, 9) 
            cell = row * 9 + column 
            while array[cell] != 0:  # Find an empty (zero) cell 
                row = random.randrange(0, 9) 
                column = random.randrange(0, 9) 
                cell = row * 9 + column        
            array[cell] = first_sudoku[cell]  # Restore the original value
            possible[cell] = first_possible[cell] 
            count_columns[column] += 1    
            count_rows[row] += 1  # Refresh row and column counts
            flag_2 = False 
            return row, column, array, possible, count_rows, count_columns, flag_2 

    return row, column, array, possible, count_rows, count_columns, flag_2


# ____________This function randomly chooses a row and a column to define a cell___________ #
def choice(count_rows, count_columns, givens): 
    """
    Randomly chooses a row and a column that has more than the minimum number of 'givens'
    to define the cell to be vacated.
    """
    row = random.randrange(0, 9) 
    while count_rows[row] <= givens: 
        row = random.randrange(0, 9) 

    column = random.randrange(0, 9) 
    while count_columns[column] <= givens: 
        column = random.randrange(0, 9) 

    return row, column


# __The role of this function is to restore the value of one zero cell and vacate another cell__ #
def vacate_another_cell(first_sudoku, first_possible, backup_sudoku, backup_possible, count_rows, count_columns, givens): 
    """
    Restores the value of one zero cell to its original state, then vacates another cell.
    Ensures that the row and column counts are updated accordingly.
    """
    row = random.randrange(0, 9) 
    column = random.randrange(0, 9) 
    cell = row * 9 + column 

    # Find a zero cell to restore
    while backup_sudoku[cell] != 0:  
        row = random.randrange(0, 9) 
        column = random.randrange(0, 9) 
        cell = row * 9 + column 

    backup_sudoku[cell] = first_sudoku[cell]  # Restore the original value
    backup_possible[cell] = first_possible[cell] 
    count_columns[column] += 1 
    count_rows[row] += 1  # Refresh row and column counts

    # Call check_1 function to vacate another cell
    row, column, backup_sudoku, backup_possible, count_rows, count_columns, flag_2 = check_1(givens, backup_sudoku, backup_possible, first_sudoku, first_possible, count_rows, count_columns, cell) 

    # Repeat until a valid cell is vacated
    while not flag_2:        
        row, column, backup_sudoku, backup_possible, count_rows, count_columns, flag_2 = check_1(givens, backup_sudoku, backup_possible, first_sudoku, first_possible, count_rows, count_columns, cell)  

    cell_new = row * 9 + column 
    backup_sudoku[cell_new] = 0  # Vacate the new cell
    backup_possible[cell_new] = [] 
    for j in range(1, 10): 
        backup_possible[cell_new].append(j)  # Add back possible values to the vacated cell
    
    count_columns[column] -= 1 
    count_rows[row] -= 1  # Refresh row and column counts
    return backup_sudoku, backup_possible, count_rows, count_columns
