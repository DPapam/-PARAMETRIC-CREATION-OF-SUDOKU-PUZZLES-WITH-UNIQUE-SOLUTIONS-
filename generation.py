#_______This file describes the whole procedure of parametric creating of sudoku puzzles _______# 
from array import * 
from collections import defaultdict 
from logic import * 
from single_solution import * 
from empty_cells import * 
from sudoku_generator import SudokuGenerator
  
backup_actual_stack = [] 
backup_possible_stack = [] 
first_actual_stack = [] 
first_possible_stack = [] 
  
  
#_______This function starts with an empty sudoku grid 9∗9 and returns a completed sudoku grid_______# 
def generate_complete(): 
    """
    Generates a complete 9x9 Sudoku grid using a Sudoku generator and returns the generated grid 
    and the corresponding array of possible values for each cell.
    """
    sudoku_gen = SudokuGenerator()
    sudoku_array = sudoku_gen.sudoku_array
    sudoku_possible = sudoku_gen.sudoku_possible
    return sudoku_array, sudoku_possible 


#_______The role of this function is to check whether the sudoku has a unique solution or not_______# 
def check_for_solution(sudoku_array, sudoku_possible, difficulty): 
    """
    Checks if the current Sudoku puzzle has a unique solution. If yes, it returns the solved puzzle,
    backup of the original puzzle, and score. Otherwise, it continues checking.
    """
    backup_actual_stack.append(sudoku_array[:])  # Backup the current sudoku grid
    backup_possible_stack.append(sudoku_possible[:])  # Backup the possible values for the current grid
    backup_sudoku = backup_actual_stack[-1]  # Create a copy of the partially completed sudoku
    backup_possible = backup_possible_stack[-1]  # Create a copy of the possible values array
    actual_stack.append(sudoku_array[:]) 
    possible_stack.append(sudoku_possible[:]) 
    sudoku_array = actual_stack[-1] 
    sudoku_possible = possible_stack[-1]  # Update the sudoku_array and sudoku_possible with the new values
    flag_sol, flag_1, sudoku_array, sudoku_possible, score = checker(sudoku_array, sudoku_possible, difficulty)  # Check for solution
    return flag_sol, flag_1, sudoku_array, sudoku_possible, backup_sudoku, backup_possible, score 


#_______The aim of this function is to vacate another cell and check again for a unique solution_______# 
def try_vacate(first_sudoku, first_possible, backup_sudoku, backup_possible, tries, count_rows, count_columns, givens, difficulty): 
    """
    Attempts to vacate another cell in the grid and checks if the puzzle still has a unique solution.
    If a unique solution is found, returns the updated puzzle. Otherwise, continues trying to vacate cells.
    """
    # Restore a zero cell and vacate another one by calling vacate_another_cell
    backup_sudoku, backup_possible, count_rows, count_columns = vacate_another_cell(first_sudoku, first_possible, backup_sudoku, backup_possible, count_rows, count_columns, givens) 
    actual_stack.append(backup_sudoku[:]) 
    possible_stack.append(backup_possible[:]) 
    sudoku_array = actual_stack[-1] 
    sudoku_possible = possible_stack[-1] 

    # Check again for a unique solution
    flag_sol, flag_1, sudoku_array, sudoku_possible, backup_sudoku, backup_possible, score = check_for_solution(sudoku_array, sudoku_possible, difficulty) 
    if flag_sol == False:  # If no unique solution is found, increment the try counter
        tries = tries + 1 
    return flag_sol, flag_1, sudoku_array, sudoku_possible, backup_sudoku, backup_possible, tries, count_rows, count_columns, score 


#_______This function checks the score and evaluates if the score responds to the chosen difficulty level_______# 
def evaluation(difficulty, score): 
    """
    Evaluates the score of the puzzle and determines if it corresponds to the chosen difficulty level.
    Returns True if the score does not match the difficulty level, prompting puzzle regeneration.
    """
    flag_gen = False 
    if difficulty == 1: 
        if score not in range(42, 47):  # Check if score falls within the range for difficulty 1
            flag_gen = True 
    elif difficulty == 2: 
        if score not in range(49, 54):  # Check if score falls within the range for difficulty 2
            flag_gen = True 
    elif difficulty == 3: 
        if score not in range(55, 61):  # Check if score falls within the range for difficulty 3
            flag_gen = True 
    elif difficulty == 4: 
        if score not in range(61, 117):  # Check if score falls within the range for difficulty 4
            flag_gen = True 
    return flag_gen 


#_______The main function includes all the steps from scratch to the generation of a valid sudoku puzzle_______#    
def generation(number, difficulty, givens): 
    """
    Main function to generate a valid Sudoku puzzle. The function generates a complete grid, 
    vacates cells according to the difficulty level, and ensures the puzzle has a unique solution.
    The process repeats until a valid puzzle is generated with the appropriate score.
    """
    flag_gen = True 
    while flag_gen: 
        sudoku_array, sudoku_possible = generate_complete()  # Generate a solution  
        actual_stack.clear() 
        possible_stack.clear() 
        actual_stack.append(sudoku_array[:]) 
        possible_stack.append(sudoku_possible[:])  # Push sudoku_array and sudoku_possible to the corresponding stacks to track changes
        first_sudoku = actual_stack[-1]           
        first_possible = possible_stack[-1]  # Copy the initial complete Sudoku and possible values
        first_actual_stack.append(first_sudoku[:]) 
        first_possible_stack.append(first_possible[:]) 
        first_sudoku = first_actual_stack[-1] 
        first_possible = first_possible_stack[-1] 
        
        sudoku_array = actual_stack[-1] 
        sudoku_possible = possible_stack[-1] 
        
        # Remove the specified "number" of cells from the Sudoku grid
        sudoku_array, sudoku_possible, count_rows, count_columns = empty_cells(number, givens, sudoku_array, sudoku_possible, first_sudoku, first_possible) 

        # Check if the puzzle has a unique solution
        flag_sol, flag_1, sudoku_array, sudoku_possible, backup_sudoku, backup_possible, score = check_for_solution(sudoku_array, sudoku_possible, difficulty) 

        # Determine what to do next based on the puzzle's state
        if flag_1 == True:  # If the puzzle was solved using logical methods only
            flag_gen = evaluation(difficulty, score)  # Check the score against the difficulty
        else:  
            if flag_sol == True:  # If the puzzle has a single solution
                flag_gen = evaluation(difficulty, score)  # Check the score
            else:  # Otherwise, vacate more cells and keep checking
                tries = 1 
                while tries < 50:  # Keep trying to vacate cells until a unique solution is found
                    flag_sol, flag_1, sudoku_array, sudoku_possible, backup_sudoku, backup_possible, tries, count_rows, count_columns, score = try_vacate(first_sudoku, first_possible, backup_sudoku, backup_possible, tries, count_rows, count_columns, givens, difficulty) 
                    if flag_sol == True: 
                        break 
                
                if tries == 50:  # If no unique solution is found after 50 tries
                    flag_gen = True  # Regenerate the puzzle 
                else: 
                    flag_gen = evaluation(difficulty, score)  # Check the score after a solution is found

        if flag_gen == False: 
            break  # Exit the loop once a valid puzzle is generated with the correct difficulty score

    return backup_sudoku, first_sudoku
