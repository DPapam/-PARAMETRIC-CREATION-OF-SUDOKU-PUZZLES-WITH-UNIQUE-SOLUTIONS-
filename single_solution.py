#____This file includes the required functions to check if the puzzle guarantees that it has a single solution ____# 
from array import * 
from collections import defaultdict 
from checking_functions import * 
from logic import * 
from brute_force_tools import *  


#__________________An auxiliary function for defining the tree lists, cell_stack, valid, empty ________________#        
def cell_choice(sudoku_array, sudoku_possible, valid, cell_stack): 
    """
    Selects the cell with the fewest possible values to try next and updates the 
    corresponding valid lists and cell_stack. This helps in finding the next cell 
    to work on while trying to find a solution.
    """
    cell = fewest_possible_values(sudoku_array, sudoku_possible)  # Find the cell with the least possible values 
    cell_stack.append([cell])  # Append the selected cell to cell_stack 
    valid.append([])  # Create an empty valid list for possible values
    for temp in sudoku_possible[cell]: 
        cell_stack[-1].append(temp) 
        valid[-1].append(temp)  # Populate valid list with possible values for the selected cell
    empty = empty_function(sudoku_array)  # Get a list of all empty cells 
    return cell_stack, valid, empty 


#_____________This function aims to find a second solution, if it fails the sudoku has one and only solution_____________# 
def brute_force_for_uniqueness(sudoku_array, sudoku_possible, count, score, solutions, valid, cell_stack, count_list_new): 
    """
    Uses brute force to search for a second solution. If no second solution is found, 
    the puzzle is guaranteed to have a single solution. This process continues by checking 
    possible values and applying backtracking if needed.
    """
    global flag_sol
    global final_flag
    flag_sol = False
    count_start = 0
    count_list_new = cells_solved_new(count, count_start)  # Count how many values confirmed using logical techniques
    count_start = count_list_new[0]
    count_list_new.clear()
    cell_stack, valid, empty = cell_choice(sudoku_array, sudoku_possible, valid, cell_stack)  # Initialize lists for solving
    final_flag = False
    flag = False

    # Try solving while the puzzle does not have a single solution
    while flag_sol == False:
        final_flag = False
        while len(empty) != 0:  # While there are still empty cells in the puzzle
            if len(cell_stack[-1]) <= 1:  # If the cell has only one possible candidate
                final_flag = True
                valid.clear()
                cell_stack.clear()
                count_list_new.clear()
                return flag_sol, sudoku_array, sudoku_possible, score

            a = range(len(cell_stack[-1]) - 1)  # Loop through possible values for the selected cell
            condition = (j for j in a if cell_stack[-1][j + 1] in valid[-1])

            for j in condition:  # Try all possible values in the valid list for the selected cell
                current_cell = cell_stack[-1][0]
                i = cell_stack[-1][j + 1]
                valid[-1].remove(i)
                if final_flag == False:
                    score += 5  # Add to the difficulty score
                    sudoku_array[current_cell] = i  # Set the value of the current cell
                    sudoku_possible[current_cell] = [i]
                    actual_stack.append(sudoku_array[:])
                    possible_stack.append(sudoku_possible[:])
                    sudoku_array = actual_stack[-1]
                    sudoku_possible = possible_stack[-1]

                    # Try solving the puzzle using logical methods
                    flag_1, error, count, score, sudoku_array, sudoku_possible = logical_methods(sudoku_array, sudoku_possible, count, score)
                    count_list_new = cells_solved_new(count, count_start)

                    if flag_1 == True:  # If a solution is found
                        solutions += 1
                        finalscore = score  # Save the score 

                        if solutions == 2:  # If a second solution is found, the puzzle has multiple solutions
                            final_flag = True
                            flag_sol = False
                            valid.clear()
                            cell_stack.clear()
                            count_list_new.clear()
                            return flag_sol, sudoku_array, sudoku_possible, score
                        else:  # If only one solution is found, continue searching for another one
                            count_last = count_list_new[-1]  # Count how many values were confirmed after guessing
                            for i in range(count_last + 2):  # Remove the confirmed states 
                                actual_stack.pop(-1)
                                possible_stack.pop(-1)
                            k = count_list_new.pop(-1)
                            count -= k

                            if j == len(cell_stack[-1]) - 2:  # If this is the last possible value for the cell
                                while True:
                                    if valid != [[]]:  # If there are still valid values to try
                                        if len(valid[-1]) == 0:  # Change the previously selected cell's value
                                            cell_stack.pop(-1)
                                            valid.pop(-1)
                                            count_prelast = count_list_new[-1]
                                            for i in range(count_prelast + 2):
                                                actual_stack.pop(-1)
                                                possible_stack.pop(-1)
                                            k = count_list_new.pop(-1)
                                            count -= k
                                        else:
                                            break
                                    else:  # If no valid values remain, the puzzle has a single solution
                                        final_flag = True
                                        flag_sol = True
                                        valid.clear()
                                        cell_stack.clear()
                                        count_list_new.clear()
                                        return flag_sol, sudoku_array, sudoku_possible, finalscore

                            sudoku_array = actual_stack[-1]
                            sudoku_possible = possible_stack[-1]
                            actual_stack.append(sudoku_array[:])
                            possible_stack.append(sudoku_possible[:])
                            flag = False
                    else:  # The Sudoku cannot be solved
                        if error == True:  # If an error occurs
                            score += 5  # Backtrack and try another value for the cell
                            count_last = count_list_new[-1]  # Remove confirmed states after the random guess
                            for i in range(count_last + 2):
                                actual_stack.pop(-1)
                                possible_stack.pop(-1)
                            k = count_list_new.pop(-1)
                            count -= k

                            if j == len(cell_stack[-1]) - 2:  # If all possible values have been tried, backtrack
                                while True:
                                    if valid != [[]]:
                                        if len(valid[-1]) == 0:
                                            cell_stack.pop(-1)
                                            valid.pop(-1)
                                            count_prelast = count_list_new[-1]
                                            for i in range(count_prelast + 2):
                                                actual_stack.pop(-1)
                                                possible_stack.pop(-1)
                                            k = count_list_new.pop(-1)
                                            count -= k
                                        else:
                                            break
                                    else:  # If no valid values remain, the puzzle has only one solution
                                        final_flag = True
                                        flag_sol = True
                                        valid.clear()
                                        cell_stack.clear()
                                        count_list_new.clear()
                                        return flag_sol, sudoku_array, sudoku_possible, score

                            sudoku_array = actual_stack[-1]
                            sudoku_possible = possible_stack[-1]
                            actual_stack.append(sudoku_array[:])
                            possible_stack.append(sudoku_possible[:])
                            flag = False
                        else:
                            sudoku_array = actual_stack[-1]
                            sudoku_possible = possible_stack[-1]
                            actual_stack.append(sudoku_array[:])
                            possible_stack.append(sudoku_possible[:])
                            cell_stack, valid, empty = cell_choice(sudoku_array, sudoku_possible, valid, cell_stack)
                            flag = True
                if final_flag == True or flag == True:
                    break
            if final_flag == True or flag == True:
                break

    valid.clear()
    cell_stack.clear()
    count_list_new.clear()
    return flag_sol, sudoku_array, sudoku_possible, score


#_____________This function determines if the sudoku guarantees that it has a single solution_____________# 
#_____________based on the chosen level of difficulty and the methods used for solving it_____________# 
def checker(sudoku_array, sudoku_possible, difficulty): 
    """
    Determines whether the Sudoku puzzle guarantees a single solution based on the 
    chosen difficulty level and the methods used for solving it.
    """
    global flag_sol  # Flag for the single solution 
    count = 0 
    solutions = 0 
    score = 0 

    # Try solving the puzzle using only logical techniques
    flag_1, error, count, score, sudoku_array, sudoku_possible = logical_methods(sudoku_array, sudoku_possible, count, score)    
    if difficulty != 4:  # For difficulty levels 1, 2, and 3, only logical methods are required 
        if flag_1 == True:  # If the puzzle was solved, it has a single solution 
            flag_sol = True 
            return flag_sol, flag_1, sudoku_array, sudoku_possible, score 
        else:  # Otherwise, the Sudoku does not meet the difficulty level
            flag_sol = False 
    else:  # For difficulty level 4
        if flag_1 == True:  # If the puzzle was solved, it has a single solution 
            flag_sol = True 
            return flag_sol, flag_1, sudoku_array, sudoku_possible, score 
        else:  # Otherwise, try guessing numbers to check for uniqueness
            valid = [] 
            cell_stack = [] 
            count_list_new = []            
            flag_sol, sudoku_array, sudoku_possible, score = brute_force_for_uniqueness(sudoku_array, sudoku_possible, count, score, solutions, valid, cell_stack, count_list_new) 
    return flag_sol, flag_1, sudoku_array, sudoku_possible, score 
