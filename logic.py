#_______________This file includes the required functions for the puzzle’s logical solving_______________#   
from array import * 
from collections import defaultdict 
from checking_functions import * 
from random import shuffle 
import sys 
from itertools import combinations
 
flag_1=False 
error=False 
global total 
total=0 
actual_stack=[] 
possible_stack=[] 
count_list=[0] 
count_list_new=[] 
 
#_______________starting function, it creates a new sudoku grid composed of 81 zero cells_______________# 
def starting(sudoku_array): 
    ''' 
    This function initializes the starting state of the Sudoku grid. 
    It creates a grid where all cells are empty (set to zero), 
    and populates the possible values for each empty cell (1-9).
    The possible values for each empty cell are shuffled to ensure randomness in the solving process.
    '''
    actual_stack.append(sudoku_array[:]) 
    a=len(sudoku_array) 
    sudoku_possible= [[] for _ in range(a)]  # 81 lists of possible values, one for each cell 
    for i in range(len(sudoku_array)): 
        if sudoku_array[i] == 0: 
            for j in range(1,10):  # If the cell is empty, the possible values of this cell are [1-9]
                sudoku_possible[i].append(j) 
            shuffle(sudoku_possible[i])  # Shuffle the possible values to add randomness
    possible_stack.append(sudoku_possible[:]) 
    sudoku_array=actual_stack[-1] 
    sudoku_possible=possible_stack[-1] 
    return (sudoku_array, sudoku_possible) 
 


#_______________Candidate Checking Method_______________#        
def candidate_checking(sudoku_array, sudoku_possible, count, score):
    global error
    counter = 0
    for i in range(len(sudoku_array)):
        if sudoku_array[i] == 0:  # Only consider empty cells
            track = set()  # Using a set for faster lookups
            current_r, current_c = divmod(i, 9)  # Get the row and column

            # Row check
            for row in range(current_c, 81, 9):  # Iterate over the row
                if len(sudoku_possible[row]) == 1 and sudoku_array[row] in sudoku_possible[i]:
                    track.add(sudoku_array[row])

            # Column check
            start_1 = i - current_c
            for col in range(start_1, start_1 + 9):
                if len(sudoku_possible[col]) == 1 and sudoku_array[col] in sudoku_possible[i] and sudoku_array[col] not in track:
                    track.add(sudoku_array[col])

            # Minigrid check
            start_r = 3 * (current_r // 3)
            start_c = 3 * (current_c // 3)
            for r in range(start_r, start_r + 3):
                for c in range(start_c, start_c + 3):
                    x = r * 9 + c
                    if len(sudoku_possible[x]) == 1 and sudoku_array[x] in sudoku_possible[i] and sudoku_array[x] not in track:
                        track.add(sudoku_array[x])

            # Update possible values for cell i
            sudoku_possible[i] = [e for e in sudoku_possible[i] if e not in track]

            # If only one possible value remains, assign it to the cell
            if len(sudoku_possible[i]) == 1:
                sudoku_array[i] = sudoku_possible[i][0]
                counter += 1
                score += 1
                count += 1
                actual_stack.append(sudoku_array[:])
                possible_stack.append(sudoku_possible[:])
                sudoku_array = actual_stack[-1]
                sudoku_possible = possible_stack[-1]

            # Error detection: if no possible values remain, flag an error
            if len(sudoku_possible[i]) == 0:
                error = True
                break

    return (counter, sudoku_array, sudoku_possible, count, score)

 

#_______________Place Finding Methods_______________# 
#_______________Place Finding in Columns_____________# 
def place_finding_columns(sudoku_array, sudoku_possible, count, score):
    flag = False
    for c in range(9):  # Iterate over columns
        for number in range(1, 10):  # Check each number from 1 to 9
            possible_positions = []  # List to store cells that can take this number
            for r in range(9):  # Iterate over rows in the column
                cell = r * 9 + c  # Convert row and column to cell index
                if sudoku_array[cell] == 0 and number in sudoku_possible[cell]:
                    possible_positions.append(cell)
                if len(possible_positions) > 1:  # If more than 1 position is found, stop checking
                    break

            # If only one position is possible, place the number
            if len(possible_positions) == 1:
                pos = possible_positions[0]
                sudoku_array[pos] = number
                sudoku_possible[pos] = [number]  # Restrict possible values to only this number
                score += 2
                count += 1
                actual_stack.append(sudoku_array[:])  # Save current state
                possible_stack.append(sudoku_possible[:])
                flag = True
                break  # Break after placing the number
        if flag:  # Stop checking further columns if a placement was made
            break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Place Finding in Rows_______________# 
def place_finding_rows(sudoku_array, sudoku_possible, count, score):
    flag = False
    for r in range(9):  # Iterate through rows
        for number in range(1, 10):  # Check numbers 1 through 9
            possible_positions = []  # List to track possible positions for the number
            for c in range(9):  # Iterate through columns in the row
                cell = r * 9 + c  # Convert row and column to a cell index
                if sudoku_array[cell] == 0 and number in sudoku_possible[cell]:
                    possible_positions.append(cell)
                if len(possible_positions) > 1:  # If more than one position is possible, stop
                    break

            # If only one possible position is found, place the number
            if len(possible_positions) == 1:
                pos = possible_positions[0]
                sudoku_array[pos] = number
                sudoku_possible[pos] = [number]  # Limit possible values to just the placed number
                score += 2
                count += 1
                actual_stack.append(sudoku_array[:])  # Save current state to the stack
                possible_stack.append(sudoku_possible[:])
                flag = True
                break  # Break after making a placement
        if flag:  # Stop if a number was placed
            break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Place Finding in Minigrids_______________# 
def place_finding_minigrids(sudoku_array, sudoku_possible, count, score):
    flag = False
    minigrid_start_positions = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # First cell of each minigrid
    for i in minigrid_start_positions:
        for number in range(1, 10):
            possible_positions = []
            start_r, start_c = divmod(i, 9)
            stop_r = start_r + 3
            stop_c = start_c + 3

            # Scan the minigrid for possible placements of the number
            for r in range(start_r, stop_r):
                for c in range(start_c, stop_c):
                    cell = r * 9 + c
                    if sudoku_array[cell] == 0 and number in sudoku_possible[cell]:
                        possible_positions.append(cell)
                    if len(possible_positions) > 1:  # If more than 1 position is found, stop
                        break

            # If exactly one possible position is found, place the number
            if len(possible_positions) == 1:
                pos = possible_positions[0]
                sudoku_array[pos] = number
                sudoku_possible[pos] = [number]
                score += 2
                count += 1
                actual_stack.append(sudoku_array[:])  # Save state
                possible_stack.append(sudoku_possible[:])
                flag = True
                break
        if flag:  # Stop if a placement was made
            break
    return flag, sudoku_array, sudoku_possible, count, score

    

#_______________Looking for Twins Methods_______________# 
#_______________Looking for Twins  in Minigrids____________# 
def twins_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []
    for i in range(len(sudoku_array)):
        if sudoku_array[i] == 0 and len(sudoku_possible[i]) == 2:  # Find a cell with exactly two possible values
            first, second = sudoku_possible[i]  # Extract the two possible values
            mylist = [first, second]
            current_r, current_c = divmod(i, 9)
            start_r = 3 * (current_r // 3)
            start_c = 3 * (current_c // 3)
            stop_r = start_r + 3
            stop_c = start_c + 3

            # Find another cell in the same minigrid with the same possible values
            for r in range(start_r, stop_r):
                for c in range(start_c, stop_c):
                    x = r * 9 + c
                    if sudoku_array[x] == 0 and len(sudoku_possible[x]) == 2 and x != i:
                        if set(sudoku_possible[x]) == set(mylist):
                            # Eliminate these values from the rest of the minigrid
                            for r2 in range(start_r, stop_r):
                                for c2 in range(start_c, stop_c):
                                    y = r2 * 9 + c2
                                    if sudoku_array[y] == 0 and y != i and y != x:
                                        track = [val for val in sudoku_possible[y] if val in mylist]
                                        if track:
                                            sudoku_possible[y] = [e for e in sudoku_possible[y] if e not in track]
                                            flag = True

                                        # Check if a cell has only one possible value and it is not in the list
                                        if len(sudoku_possible[y]) == 1 and sudoku_possible[y][0] not in v_list:
                                            sudoku_array[y] = sudoku_possible[y][0]
                                            v_list.append(sudoku_array[y])
                                            score += 3
                                            count += 1
                                            actual_stack.append(sudoku_array[:])
                                            possible_stack.append(sudoku_possible[:])
                                        elif len(sudoku_possible[y]) == 1 and sudoku_possible[y][0] in v_list:
                                            error = True
                                            return flag, sudoku_array, sudoku_possible, count, score

                                        # Error detection: if no possible values remain
                                        if len(sudoku_possible[y]) == 0:
                                            error = True
                                            return flag, sudoku_array, sudoku_possible, count, score
                            break
                if flag:  # Exit after processing a valid pair
                    break
            if flag:
                break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Looking for Twins in Rows_______________#     
def twins_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []
    
    for r in range(9):  # Iterate through each row
        for c in range(9):  # Iterate through each cell in the row
            cell = r * 9 + c
            if sudoku_array[cell] == 0 and len(sudoku_possible[cell]) == 2:  # Look for cells with exactly 2 possibilities
                first, second = sudoku_possible[cell]  # Extract the two possible values
                mylist = [first, second]

                # Look for another cell in the same row with the same two possible values
                for c2 in range(9):
                    other_cell = r * 9 + c2
                    if sudoku_array[other_cell] == 0 and len(sudoku_possible[other_cell]) == 2 and other_cell != cell:
                        if set(sudoku_possible[other_cell]) == set(mylist):
                            # Eliminate these values from other cells in the row
                            for c3 in range(9):
                                check_cell = r * 9 + c3
                                if sudoku_array[check_cell] == 0 and check_cell != cell and check_cell != other_cell:
                                    track = [val for val in sudoku_possible[check_cell] if val in mylist]
                                    if track:
                                        sudoku_possible[check_cell] = [e for e in sudoku_possible[check_cell] if e not in track]
                                        flag = True

                                    # If only one possible value remains, place it in the cell
                                    if len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] not in v_list:
                                        sudoku_array[check_cell] = sudoku_possible[check_cell][0]
                                        v_list.append(sudoku_array[check_cell])
                                        score += 3
                                        count += 1
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])
                                    elif len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] in v_list:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

                                    # Error detection: if no possible values remain
                                    if len(sudoku_possible[check_cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score
                            break
            if flag:  # Stop if twins are found and processed
                break
        if flag:
            break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Looking for Twins in Columns_______________#     
def twins_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []

    for c in range(9):  # Iterate through each column
        for r in range(9):  # Iterate through each cell in the column
            cell = r * 9 + c
            if sudoku_array[cell] == 0 and len(sudoku_possible[cell]) == 2:  # Look for cells with exactly 2 possibilities
                first, second = sudoku_possible[cell]  # Extract the two possible values
                mylist = [first, second]

                # Look for another cell in the same column with the same two possible values
                for r2 in range(9):
                    other_cell = r2 * 9 + c
                    if sudoku_array[other_cell] == 0 and len(sudoku_possible[other_cell]) == 2 and other_cell != cell:
                        if set(sudoku_possible[other_cell]) == set(mylist):
                            # Eliminate these values from other cells in the column
                            for r3 in range(9):
                                check_cell = r3 * 9 + c
                                if sudoku_array[check_cell] == 0 and check_cell != cell and check_cell != other_cell:
                                    track = [val for val in sudoku_possible[check_cell] if val in mylist]
                                    if track:
                                        sudoku_possible[check_cell] = [e for e in sudoku_possible[check_cell] if e not in track]
                                        flag = True

                                    # If only one possible value remains, place it in the cell
                                    if len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] not in v_list:
                                        sudoku_array[check_cell] = sudoku_possible[check_cell][0]
                                        v_list.append(sudoku_array[check_cell])
                                        score += 3
                                        count += 1
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])
                                    elif len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] in v_list:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

                                    # Error detection: if no possible values remain
                                    if len(sudoku_possible[check_cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score
                            break
            if flag:  # Stop if twins are found and processed
                break
        if flag:
            break
    return flag, sudoku_array, sudoku_possible, count, score



#_______________Looking for Hidden Twins Methods_______________#
#_______________Looking for Hidden Twins in Rows_______________#
def hidden_twins_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for r in range(9):  # Iterate over all rows
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for c in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(c)  # Track columns where this candidate is possible

        # Find hidden twins: two candidates appearing in exactly two cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 2:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:  # Check if two candidates share exactly two cells
                        # We found a hidden twin: candidate1 and candidate2 must be in these two cells
                        for cell in cells1:
                            if set(sudoku_possible[r * 9 + cell]) != {candidate1, candidate2}:
                                # Eliminate other candidates from these two cells
                                before = len(sudoku_possible[r * 9 + cell])
                                sudoku_possible[r * 9 + cell] = [candidate for candidate in sudoku_possible[r * 9 + cell] if candidate in {candidate1, candidate2}]
                                after = len(sudoku_possible[r * 9 + cell])

                                if before != after:
                                    flag = True
                                    score += 4

                                    # If only one candidate remains, place it in the cell
                                    if len(sudoku_possible[r * 9 + cell]) == 1:
                                        sudoku_array[r * 9 + cell] = sudoku_possible[r * 9 + cell][0]
                                        count += 1
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])

                                    # Error detection: if no candidates remain
                                    if len(sudoku_possible[r * 9 + cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Twins in Columns_______________#     

def hidden_twins_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for c in range(9):  # Iterate over all columns
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for r in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(r)  # Track rows where this candidate is possible

        # Find hidden twins: two candidates appearing in exactly two cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 2:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:  # Check if two candidates share exactly two cells
                        # We found a hidden twin: candidate1 and candidate2 must be in these two cells
                        for cell in cells1:
                            if set(sudoku_possible[cell * 9 + c]) != {candidate1, candidate2}:
                                # Eliminate other candidates from these two cells
                                before = len(sudoku_possible[cell * 9 + c])
                                sudoku_possible[cell * 9 + c] = [candidate for candidate in sudoku_possible[cell * 9 + c] if candidate in {candidate1, candidate2}]
                                after = len(sudoku_possible[cell * 9 + c])

                                if before != after:
                                    flag = True
                                    score += 4

                                    # If only one candidate remains, place it in the cell
                                    if len(sudoku_possible[cell * 9 + c]) == 1:
                                        sudoku_array[cell * 9 + c] = sudoku_possible[cell * 9 + c][0]
                                        count += 1
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])

                                    # Error detection: if no candidates remain
                                    if len(sudoku_possible[cell * 9 + c]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Twins  in Minigrids____________#
def hidden_twins_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    minigrid_start_positions = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting index of each minigrid

    for i in minigrid_start_positions:
        candidate_count = defaultdict(list)
        start_r, start_c = divmod(i, 9)

        # Correct the start row and column for 3x3 traversal
        start_r = (start_r // 3) * 3  # Ensure we start at the correct minigrid row
        start_c = (start_c // 3) * 3  # Ensure we start at the correct minigrid column

        # Traverse the 3x3 minigrid
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                cell = r * 9 + c
                if sudoku_array[cell] == 0:  # If the cell is unsolved
                    for candidate in sudoku_possible[cell]:
                        candidate_count[candidate].append(cell)

        # Find hidden twins: two candidates appearing in exactly two cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 2:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for cell in cells1:
                            if set(sudoku_possible[cell]) != {candidate1, candidate2}:
                                # Eliminate other candidates from these two cells
                                before = len(sudoku_possible[cell])
                                sudoku_possible[cell] = [candidate for candidate in sudoku_possible[cell] if candidate in {candidate1, candidate2}]
                                after = len(sudoku_possible[cell])

                                if before != after:
                                    flag = True
                                    score += 4

                                    # If only one candidate remains, place it in the cell
                                    if len(sudoku_possible[cell]) == 1:
                                        sudoku_array[cell] = sudoku_possible[cell][0]
                                        count += 1
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])

                                    # Error detection: if no candidates remain
                                    if len(sudoku_possible[cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score



 
#_______________Looking for Triplets Methods_______________# 
#_______________Looking for Triplets in Minigrids_______________# 
def triplets_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []
    for i in range(len(sudoku_array)):
        if sudoku_array[i] == 0 and len(sudoku_possible[i]) == 2 or len(sudoku_possible[i]) == 3:  # Find cells with 2 or 3 possible values
            possible_vals = sudoku_possible[i]
            current_r, current_c = divmod(i, 9)
            start_r = 3 * (current_r // 3)
            start_c = 3 * (current_c // 3)
            stop_r = start_r + 3
            stop_c = start_c + 3

            # Find other cells in the same minigrid with the same possible values
            matching_cells = []
            for r in range(start_r, stop_r):
                for c in range(start_c, stop_c):
                    x = r * 9 + c
                    if sudoku_array[x] == 0 and len(sudoku_possible[x]) in [2, 3] and x != i:
                        if set(sudoku_possible[x]).issubset(set(possible_vals)):
                            matching_cells.append(x)

            # If there are exactly two other matching cells (total 3), perform elimination
            if len(matching_cells) == 2:
                # Eliminate these values from the rest of the minigrid
                for r2 in range(start_r, stop_r):
                    for c2 in range(start_c, stop_c):
                        y = r2 * 9 + c2
                        if sudoku_array[y] == 0 and y not in [i] + matching_cells:
                            track = [val for val in sudoku_possible[y] if val in possible_vals]
                            if track:
                                sudoku_possible[y] = [e for e in sudoku_possible[y] if e not in track]
                                flag = True

                            # If only one possible value remains, place it in the cell
                            if len(sudoku_possible[y]) == 1 and sudoku_possible[y][0] not in v_list:
                                sudoku_array[y] = sudoku_possible[y][0]
                                v_list.append(sudoku_array[y])
                                score += 4
                                count += 1
                                actual_stack.append(sudoku_array[:])
                                possible_stack.append(sudoku_possible[:])
                            elif len(sudoku_possible[y]) == 1 and sudoku_possible[y][0] in v_list:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score

                            # Error detection: if no possible values remain
                            if len(sudoku_possible[y]) == 0:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score
                break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Looking for Triplets in Rows_______________#     
def triplets_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []

    for r in range(9):  # Iterate through each row
        for c in range(9):  # Iterate through each cell in the row
            cell = r * 9 + c
            if sudoku_array[cell] == 0 and len(sudoku_possible[cell]) in [2, 3]:  # Look for cells with 2 or 3 possibilities
                possible_vals = sudoku_possible[cell]

                # Find other cells in the same row with the same possible values
                matching_cells = []
                for c2 in range(9):
                    other_cell = r * 9 + c2
                    if sudoku_array[other_cell] == 0 and len(sudoku_possible[other_cell]) in [2, 3] and other_cell != cell:
                        if set(sudoku_possible[other_cell]).issubset(set(possible_vals)):
                            matching_cells.append(other_cell)

                # If exactly two other matching cells are found (total 3), perform elimination
                if len(matching_cells) == 2:
                    # Eliminate these values from the rest of the row
                    for c3 in range(9):
                        check_cell = r * 9 + c3
                        if sudoku_array[check_cell] == 0 and check_cell not in [cell] + matching_cells:
                            track = [val for val in sudoku_possible[check_cell] if val in possible_vals]
                            if track:
                                sudoku_possible[check_cell] = [e for e in sudoku_possible[check_cell] if e not in track]
                                flag = True

                            # If only one possible value remains, place it in the cell
                            if len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] not in v_list:
                                sudoku_array[check_cell] = sudoku_possible[check_cell][0]
                                v_list.append(sudoku_array[check_cell])
                                score += 4
                                count += 1
                                actual_stack.append(sudoku_array[:])
                                possible_stack.append(sudoku_possible[:])
                            elif len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] in v_list:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score

                            # Error detection: if no possible values remain
                            if len(sudoku_possible[check_cell]) == 0:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score
                    break
        if flag:
            break
    return flag, sudoku_array, sudoku_possible, count, score

 
#_______________Looking for Triplets in Columns_______________# 
def triplets_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    v_list = []

    for c in range(9):  # Iterate through each column
        for r in range(9):  # Iterate through each cell in the column
            cell = r * 9 + c
            if sudoku_array[cell] == 0 and len(sudoku_possible[cell]) in [2, 3]:  # Look for cells with 2 or 3 possibilities
                possible_vals = sudoku_possible[cell]

                # Find other cells in the same column with the same possible values
                matching_cells = []
                for r2 in range(9):
                    other_cell = r2 * 9 + c
                    if sudoku_array[other_cell] == 0 and len(sudoku_possible[other_cell]) in [2, 3] and other_cell != cell:
                        if set(sudoku_possible[other_cell]).issubset(set(possible_vals)):
                            matching_cells.append(other_cell)

                # If exactly two other matching cells are found (total 3), perform elimination
                if len(matching_cells) == 2:
                    # Eliminate these values from the rest of the column
                    for r3 in range(9):
                        check_cell = r3 * 9 + c
                        if sudoku_array[check_cell] == 0 and check_cell not in [cell] + matching_cells:
                            track = [val for val in sudoku_possible[check_cell] if val in possible_vals]
                            if track:
                                sudoku_possible[check_cell] = [e for e in sudoku_possible[check_cell] if e not in track]
                                flag = True

                            # If only one possible value remains, place it in the cell
                            if len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] not in v_list:
                                sudoku_array[check_cell] = sudoku_possible[check_cell][0]
                                v_list.append(sudoku_array[check_cell])
                                score += 4
                                count += 1
                                actual_stack.append(sudoku_array[:])
                                possible_stack.append(sudoku_possible[:])
                            elif len(sudoku_possible[check_cell]) == 1 and sudoku_possible[check_cell][0] in v_list:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score

                            # Error detection: if no possible values remain
                            if len(sudoku_possible[check_cell]) == 0:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score
                    break
        if flag:
            break
    return flag, sudoku_array, sudoku_possible, count, score



#_______________Looking for Hidden Triplets Methods_______________#
#_______________Looking for Hidden Triplets in Rows_______________#
def hidden_triplets_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for r in range(9):  # Iterate over all rows
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for c in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(c)  # Track columns where this candidate is possible

        # Find hidden triplets: three candidates appearing in exactly three cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 3:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                # We found a hidden triplet: candidate1, candidate2, and candidate3 must be in these three cells
                                for cell in cells1:
                                    if not set(sudoku_possible[r * 9 + cell]) <= {candidate1, candidate2, candidate3}:
                                        # Eliminate other candidates from these three cells
                                        before = len(sudoku_possible[r * 9 + cell])
                                        sudoku_possible[r * 9 + cell] = [candidate for candidate in sudoku_possible[r * 9 + cell] if candidate in {candidate1, candidate2, candidate3}]
                                        after = len(sudoku_possible[r * 9 + cell])

                                        if before != after:
                                            flag = True
                                            score += 4

                                            # If only one candidate remains, place it in the cell
                                            if len(sudoku_possible[r * 9 + cell]) == 1:
                                                sudoku_array[r * 9 + cell] = sudoku_possible[r * 9 + cell][0]
                                                count += 1
                                                actual_stack.append(sudoku_array[:])
                                                possible_stack.append(sudoku_possible[:])

                                            # Error detection: if no candidates remain
                                            if len(sudoku_possible[r * 9 + cell]) == 0:
                                                error = True
                                                return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Triplets in Columns_______________#
def hidden_triplets_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for c in range(9):  # Iterate over all columns
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for r in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(r)  # Track rows where this candidate is possible

        # Find hidden triplets: three candidates appearing in exactly three cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 3:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                # We found a hidden triplet: candidate1, candidate2, and candidate3 must be in these three cells
                                for cell in cells1:
                                    if not set(sudoku_possible[cell * 9 + c]) <= {candidate1, candidate2, candidate3}:
                                        # Eliminate other candidates from these three cells
                                        before = len(sudoku_possible[cell * 9 + c])
                                        sudoku_possible[cell * 9 + c] = [candidate for candidate in sudoku_possible[cell * 9 + c] if candidate in {candidate1, candidate2, candidate3}]
                                        after = len(sudoku_possible[cell * 9 + c])

                                        if before != after:
                                            flag = True
                                            score += 4

                                            # If only one candidate remains, place it in the cell
                                            if len(sudoku_possible[cell * 9 + c]) == 1:
                                                sudoku_array[cell * 9 + c] = sudoku_possible[cell * 9 + c][0]
                                                count += 1
                                                actual_stack.append(sudoku_array[:])
                                                possible_stack.append(sudoku_possible[:])

                                            # Error detection: if no candidates remain
                                            if len(sudoku_possible[cell * 9 + c]) == 0:
                                                error = True
                                                return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Triplets in Minigrids_______________#
def hidden_triplets_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    minigrid_start_positions = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting index of each minigrid

    for i in minigrid_start_positions:
        candidate_count = defaultdict(list)
        start_r, start_c = divmod(i, 9)

        # Correct the start row and column for 3x3 traversal
        start_r = (start_r // 3) * 3  # Ensure we start at the correct minigrid row
        start_c = (start_c // 3) * 3  # Ensure we start at the correct minigrid column

        # Traverse the 3x3 minigrid
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                cell = r * 9 + c
                if sudoku_array[cell] == 0:  # If the cell is unsolved
                    for candidate in sudoku_possible[cell]:
                        candidate_count[candidate].append(cell)

        # Find hidden triplets: three candidates appearing in exactly three cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 3:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                # We found a hidden triplet: candidate1, candidate2, and candidate3 must be in these three cells
                                for cell in cells1:
                                    if not set(sudoku_possible[cell]) <= {candidate1, candidate2, candidate3}:
                                        # Eliminate other candidates from these three cells
                                        before = len(sudoku_possible[cell])
                                        sudoku_possible[cell] = [candidate for candidate in sudoku_possible[cell] if candidate in {candidate1, candidate2, candidate3}]
                                        after = len(sudoku_possible[cell])

                                        if before != after:
                                            flag = True
                                            score += 4

                                            # If only one candidate remains, place it in the cell
                                            if len(sudoku_possible[cell]) == 1:
                                                sudoku_array[cell] = sudoku_possible[cell][0]
                                                count += 1
                                                actual_stack.append(sudoku_array[:])
                                                possible_stack.append(sudoku_possible[:])

                                            # Error detection: if no candidates remain
                                            if len(sudoku_possible[cell]) == 0:
                                                error = True
                                                return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score



#_______________Looking for Quads Methods_______________# 
#_______________Looking for Quads in Rows_______________#
def naked_quads_in_rows(sudoku_array, sudoku_possible, count, score):
    """
    Identifies naked quads in rows and eliminates their candidates from other cells in the same row.
    """
    global error
    flag = False
    size = 9

    for row in range(size):
        # Gather unsolved cells and their candidates in the row
        candidates_in_row = [(col, sudoku_possible[row * size + col]) for col in range(size) if sudoku_array[row * size + col] == 0]
        if len(candidates_in_row) < 4:
            continue

        # Check for naked quads: four cells sharing only four candidates
        for (col1, candidates1), (col2, candidates2), (col3, candidates3), (col4, candidates4) in combinations(candidates_in_row, 4):
            combined_candidates = set(candidates1) | set(candidates2) | set(candidates3) | set(candidates4)

            if len(combined_candidates) == 4:  # It's a naked quad!
                # Eliminate these candidates from other cells in the row
                for col in range(size):
                    if col not in [col1, col2, col3, col4] and sudoku_array[row * size + col] == 0:
                        cell = row * size + col
                        before = len(sudoku_possible[cell])
                        sudoku_possible[cell] = [c for c in sudoku_possible[cell] if c not in combined_candidates]
                        after = len(sudoku_possible[cell])

                        if before != after:  # If a change was made
                            flag = True
                            score += 4

                            # If only one candidate remains, place it in the sudoku_array
                            if len(sudoku_possible[cell]) == 1:
                                sudoku_array[cell] = sudoku_possible[cell][0]
                                count += 1
                                actual_stack.append(sudoku_array[:])
                                possible_stack.append(sudoku_possible[:])

                            # Error detection: if no candidates remain
                            if len(sudoku_possible[cell]) == 0:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Quads in Columns_______________#     
def naked_quads_in_columns(sudoku_array, sudoku_possible, count, score):
    """
    Identifies naked quads in columns and eliminates their candidates from other cells in the same column.
    """
    global error
    flag = False
    size = 9

    for col in range(size):
        # Gather unsolved cells and their candidates in the column
        candidates_in_column = [(row, sudoku_possible[row * size + col]) for row in range(size) if sudoku_array[row * size + col] == 0]
        if len(candidates_in_column) < 4:
            continue

        # Check for naked quads: four cells sharing only four candidates
        for (row1, candidates1), (row2, candidates2), (row3, candidates3), (row4, candidates4) in combinations(candidates_in_column, 4):
            combined_candidates = set(candidates1) | set(candidates2) | set(candidates3) | set(candidates4)

            if len(combined_candidates) == 4:  # It's a naked quad!
                # Eliminate these candidates from other cells in the column
                for row in range(size):
                    if row not in [row1, row2, row3, row4] and sudoku_array[row * size + col] == 0:
                        cell = row * size + col
                        before = len(sudoku_possible[cell])
                        sudoku_possible[cell] = [c for c in sudoku_possible[cell] if c not in combined_candidates]
                        after = len(sudoku_possible[cell])

                        if before != after:  # If a change was made
                            flag = True
                            score += 4

                            # If only one candidate remains, place it in the sudoku_array
                            if len(sudoku_possible[cell]) == 1:
                                sudoku_array[cell] = sudoku_possible[cell][0]
                                count += 1
                                actual_stack.append(sudoku_array[:])
                                possible_stack.append(sudoku_possible[:])

                            # Error detection: if no candidates remain
                            if len(sudoku_possible[cell]) == 0:
                                error = True
                                return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Quads in Minigrids_______________#
def naked_quads_in_minigrids(sudoku_array, sudoku_possible, count, score):
    """
    Identifies naked quads in minigrids and eliminates their candidates from other cells in the same minigrid.
    """
    global error
    flag = False
    size = 9
    minigrid_indices = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting index of each minigrid

    for grid_start in minigrid_indices:
        grid_r, grid_c = divmod(grid_start, size)
        grid_r *= 3
        grid_c *= 3

        # Gather unsolved cells and their candidates in the minigrid
        candidates_in_minigrid = [(r, c, sudoku_possible[r * size + c]) 
                                  for r in range(grid_r, grid_r + 3) 
                                  for c in range(grid_c, grid_c + 3) 
                                  if 0 <= r * size + c < len(sudoku_possible) and sudoku_array[r * size + c] == 0]
        
        # Ensure we have at least 4 unsolved cells before checking for quads
        if len(candidates_in_minigrid) < 4:
            continue

        # Check for naked quads: four cells sharing only four candidates
        for (r1, c1, candidates1), (r2, c2, candidates2), (r3, c3, candidates3), (r4, c4, candidates4) in combinations(candidates_in_minigrid, 4):
            combined_candidates = set(candidates1) | set(candidates2) | set(candidates3) | set(candidates4)

            if len(combined_candidates) == 4:  # It's a naked quad!
                # Eliminate these candidates from other cells in the minigrid
                for r in range(grid_r, grid_r + 3):
                    for c in range(grid_c, grid_c + 3):
                        cell = r * size + c
                        if cell < len(sudoku_possible) and (r, c) not in [(r1, c1), (r2, c2), (r3, c3), (r4, c4)] and sudoku_array[cell] == 0:
                            before = len(sudoku_possible[cell])
                            sudoku_possible[cell] = [candidate for candidate in sudoku_possible[cell] if candidate not in combined_candidates]
                            after = len(sudoku_possible[cell])

                            if before != after:  # If a change was made
                                flag = True
                                score += 4

                                # If only one candidate remains, place it in the sudoku_array
                                if len(sudoku_possible[cell]) == 1:
                                    sudoku_array[cell] = sudoku_possible[cell][0]
                                    count += 1
                                    actual_stack.append(sudoku_array[:])
                                    possible_stack.append(sudoku_possible[:])

                                # Error detection: if no candidates remain
                                if len(sudoku_possible[cell]) == 0:
                                    error = True
                                    return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score



#_______________Looking for Hidden Quads Methods_______________# 
#_______________Looking for Hidden Quads in Rows_______________#
def hidden_quads_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for r in range(9):  # Iterate over all rows
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for c in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(c)  # Track columns where this candidate is possible

        # Find hidden quads: four candidates appearing in exactly four cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 4:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                for candidate4, cells4 in candidate_count.items():
                                    if candidate1 != candidate4 and candidate2 != candidate4 and candidate3 != candidate4 and cells1 == cells4:
                                        # We found a hidden quad: candidate1, candidate2, candidate3, and candidate4 must be in these four cells
                                        for cell in cells1:
                                            if not set(sudoku_possible[r * 9 + cell]) <= {candidate1, candidate2, candidate3, candidate4}:
                                                # Eliminate other candidates from these four cells
                                                before = len(sudoku_possible[r * 9 + cell])
                                                sudoku_possible[r * 9 + cell] = [candidate for candidate in sudoku_possible[r * 9 + cell] if candidate in {candidate1, candidate2, candidate3, candidate4}]
                                                after = len(sudoku_possible[r * 9 + cell])

                                                if before != after:
                                                    flag = True
                                                    score += 4

                                                    # If only one candidate remains, place it in the cell
                                                    if len(sudoku_possible[r * 9 + cell]) == 1:
                                                        sudoku_array[r * 9 + cell] = sudoku_possible[r * 9 + cell][0]
                                                        count += 1
                                                        actual_stack.append(sudoku_array[:])
                                                        possible_stack.append(sudoku_possible[:])

                                                    # Error detection: if no candidates remain
                                                    if len(sudoku_possible[r * 9 + cell]) == 0:
                                                        error = True
                                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Quads in Columns_______________# 
def hidden_quads_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False

    for c in range(9):  # Iterate over all columns
        candidate_count = defaultdict(list)  # Track where each candidate appears
        for r in range(9):
            if sudoku_array[r * 9 + c] == 0:  # If the cell is unsolved
                for candidate in sudoku_possible[r * 9 + c]:
                    candidate_count[candidate].append(r)  # Track rows where this candidate is possible

        # Find hidden quads: four candidates appearing in exactly four cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 4:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                for candidate4, cells4 in candidate_count.items():
                                    if candidate1 != candidate4 and candidate2 != candidate4 and candidate3 != candidate4 and cells1 == cells4:
                                        # We found a hidden quad: candidate1, candidate2, candidate3, and candidate4 must be in these four cells
                                        for cell in cells1:
                                            if not set(sudoku_possible[cell * 9 + c]) <= {candidate1, candidate2, candidate3, candidate4}:
                                                # Eliminate other candidates from these four cells
                                                before = len(sudoku_possible[cell * 9 + c])
                                                sudoku_possible[cell * 9 + c] = [candidate for candidate in sudoku_possible[cell * 9 + c] if candidate in {candidate1, candidate2, candidate3, candidate4}]
                                                after = len(sudoku_possible[cell * 9 + c])

                                                if before != after:
                                                    flag = True
                                                    score += 4

                                                    # If only one candidate remains, place it in the cell
                                                    if len(sudoku_possible[cell * 9 + c]) == 1:
                                                        sudoku_array[cell * 9 + c] = sudoku_possible[cell * 9 + c][0]
                                                        count += 1
                                                        actual_stack.append(sudoku_array[:])
                                                        possible_stack.append(sudoku_possible[:])

                                                    # Error detection: if no candidates remain
                                                    if len(sudoku_possible[cell * 9 + c]) == 0:
                                                        error = True
                                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score


#_______________Looking for Hidden Quads in Minigrids_______________#
def hidden_quads_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    minigrid_start_positions = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting index of each minigrid

    for i in minigrid_start_positions:
        candidate_count = defaultdict(list)
        start_r, start_c = divmod(i, 9)

        # Correct the start row and column for 3x3 traversal
        start_r = (start_r // 3) * 3  # Ensure we start at the correct minigrid row
        start_c = (start_c // 3) * 3  # Ensure we start at the correct minigrid column

        # Traverse the 3x3 minigrid
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                cell = r * 9 + c
                if sudoku_array[cell] == 0:  # If the cell is unsolved
                    for candidate in sudoku_possible[cell]:
                        candidate_count[candidate].append(cell)

        # Find hidden quads: four candidates appearing in exactly four cells
        for candidate1, cells1 in candidate_count.items():
            if len(cells1) == 4:
                for candidate2, cells2 in candidate_count.items():
                    if candidate1 != candidate2 and cells1 == cells2:
                        for candidate3, cells3 in candidate_count.items():
                            if candidate1 != candidate3 and candidate2 != candidate3 and cells1 == cells3:
                                for candidate4, cells4 in candidate_count.items():
                                    if candidate1 != candidate4 and candidate2 != candidate4 and candidate3 != candidate4 and cells1 == cells4:
                                        # We found a hidden quad: candidate1, candidate2, candidate3, and candidate4 must be in these four cells
                                        for cell in cells1:
                                            if not set(sudoku_possible[cell]) <= {candidate1, candidate2, candidate3, candidate4}:
                                                # Eliminate other candidates from these four cells
                                                before = len(sudoku_possible[cell])
                                                sudoku_possible[cell] = [candidate for candidate in sudoku_possible[cell] if candidate in {candidate1, candidate2, candidate3, candidate4}]
                                                after = len(sudoku_possible[cell])

                                                if before != after:
                                                    flag = True
                                                    score += 4

                                                    # If only one candidate remains, place it in the cell
                                                    if len(sudoku_possible[cell]) == 1:
                                                        sudoku_array[cell] = sudoku_possible[cell][0]
                                                        count += 1
                                                        actual_stack.append(sudoku_array[:])
                                                        possible_stack.append(sudoku_possible[:])

                                                    # Error detection: if no candidates remain
                                                    if len(sudoku_possible[cell]) == 0:
                                                        error = True
                                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score



#_______________X-Wing Methods_______________#
#_______________X-Wing Methods in Rows_______________#
def xwing_in_rows(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    size = 9
    
    # X-Wing for rows
    for candidate in range(1, 10):
        row_occurrences = []
        for row in range(size):
            # Find columns where candidate appears exactly twice in a row
            cols_with_candidate = [col for col in range(size) if candidate in sudoku_possible[row * size + col]]
            if len(cols_with_candidate) == 2:
                row_occurrences.append((row, cols_with_candidate))
        
        # If X-Wing pattern is found, remove candidate from other rows
        for (row1, cols1), (row2, cols2) in combinations(row_occurrences, 2):
            if cols1 == cols2:  # Matching columns, forming X-Wing
                col1, col2 = cols1
                for row in range(size):
                    if row != row1 and row != row2:
                        for col in [col1, col2]:
                            cell = row * size + col
                            if candidate in sudoku_possible[cell]:
                                sudoku_possible[cell].remove(candidate)
                                flag = True  # Candidate elimination occurred
                                
                                # If only one possible candidate remains, update sudoku_array
                                if len(sudoku_possible[cell]) == 1:
                                    sudoku_array[cell] = sudoku_possible[cell][0]
                                    score += 4  # Increment score for placing a value
                                    count += 1  # Increment count for placing a value
                                    actual_stack.append(sudoku_array[:])
                                    possible_stack.append(sudoku_possible[:])
                                
                                # Error detection: if no possible values remain
                                if len(sudoku_possible[cell]) == 0:
                                    error = True
                                    return flag, sudoku_array, sudoku_possible, count, score
    
    return flag, sudoku_array, sudoku_possible, count, score


#_______________X-Wing Methods in Columns_______________#
def xwing_in_columns(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    size = 9
    
    # X-Wing for columns
    for candidate in range(1, 10):
        col_occurrences = []
        for col in range(size):
            # Find rows where candidate appears exactly twice in a column
            rows_with_candidate = [row for row in range(size) if candidate in sudoku_possible[row * size + col]]
            if len(rows_with_candidate) == 2:
                col_occurrences.append((col, rows_with_candidate))
        
        # If X-Wing pattern is found, remove candidate from other columns
        for (col1, rows1), (col2, rows2) in combinations(col_occurrences, 2):
            if rows1 == rows2:  # Matching rows, forming X-Wing
                row1, row2 = rows1
                for col in range(size):
                    if col != col1 and col != col2:
                        for row in [row1, row2]:
                            cell = row * size + col
                            if candidate in sudoku_possible[cell]:
                                sudoku_possible[cell].remove(candidate)
                                flag = True  # Candidate elimination occurred
                                
                                # If only one possible candidate remains, update sudoku_array
                                if len(sudoku_possible[cell]) == 1:
                                    sudoku_array[cell] = sudoku_possible[cell][0]
                                    score += 4  # Increment score for placing a value
                                    count += 1  # Increment count for placing a value
                                    actual_stack.append(sudoku_array[:])
                                    possible_stack.append(sudoku_possible[:])
                                
                                # Error detection: if no possible values remain
                                if len(sudoku_possible[cell]) == 0:
                                    error = True
                                    return flag, sudoku_array, sudoku_possible, count, score
    
    return flag, sudoku_array, sudoku_possible, count, score


#_______________X-Wing Methods in Minigrids_______________#
def xwing_in_minigrids(sudoku_array, sudoku_possible, count, score):
    global error
    flag = False
    size = 9
    minigrid_indices = [0, 3, 6, 27, 30, 33, 54, 57, 60]  # Starting index of each minigrid
    
    for candidate in range(1, 10):
        for grid_start in minigrid_indices:
            grid_r, grid_c = divmod(grid_start, size)
            grid_r *= 3
            grid_c *= 3
            
            # Check boundaries before continuing
            if grid_r + 3 > size or grid_c + 3 > size:
                continue
            
            rows_in_grid = []
            cols_in_grid = []
            
            # Check if candidate appears exactly twice in rows or columns of the minigrid
            for r in range(grid_r, grid_r + 3):
                candidate_cols = [c for c in range(grid_c, grid_c + 3) if r * size + c < len(sudoku_possible) and candidate in sudoku_possible[r * size + c]]
                if len(candidate_cols) == 2:
                    rows_in_grid.append((r, candidate_cols))
                    
            for c in range(grid_c, grid_c + 3):
                candidate_rows = [r for r in range(grid_r, grid_r + 3) if r * size + c < len(sudoku_possible) and candidate in sudoku_possible[r * size + c]]
                if len(candidate_rows) == 2:
                    cols_in_grid.append((c, candidate_rows))
                    
            # Eliminate candidates from rows/columns outside the minigrid if X-Wing is detected
            for (row1, cols1), (row2, cols2) in combinations(rows_in_grid, 2):
                if cols1 == cols2:
                    col1, col2 = cols1
                    for row in range(size):
                        if row != row1 and row != row2:
                            for col in [col1, col2]:
                                cell = row * size + col
                                if cell < len(sudoku_possible) and candidate in sudoku_possible[cell]:
                                    sudoku_possible[cell].remove(candidate)
                                    flag = True
                                    
                                    # If only one possible candidate remains, update sudoku_array
                                    if len(sudoku_possible[cell]) == 1:
                                        sudoku_array[cell] = sudoku_possible[cell][0]
                                        score += 4  # Increment score for placing a value
                                        count += 1  # Increment count for placing a value
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])
                                    
                                    # Error detection: if no possible values remain
                                    if len(sudoku_possible[cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score
            
            for (col1, rows1), (col2, rows2) in combinations(cols_in_grid, 2):
                if rows1 == rows2:
                    row1, row2 = rows1
                    for col in range(size):
                        if col != col1 and col != col2:
                            for row in [row1, row2]:
                                cell = row * size + col
                                if cell < len(sudoku_possible) and candidate in sudoku_possible[cell]:
                                    sudoku_possible[cell].remove(candidate)
                                    flag = True
                                    
                                    # If only one possible candidate remains, update sudoku_array
                                    if len(sudoku_possible[cell]) == 1:
                                        sudoku_array[cell] = sudoku_possible[cell][0]
                                        score += 4  # Increment score for placing a value
                                        count += 1  # Increment count for placing a value
                                        actual_stack.append(sudoku_array[:])
                                        possible_stack.append(sudoku_possible[:])
                                    
                                    # Error detection: if no possible values remain
                                    if len(sudoku_possible[cell]) == 0:
                                        error = True
                                        return flag, sudoku_array, sudoku_possible, count, score

    return flag, sudoku_array, sudoku_possible, count, score





 
#________________________________ SOLVING ALGORITH WITH ALL LOGICAL SOLVING TECHNIQUES_______________# 
def logical_methods(sudoku_array, sudoku_possible, count, score):
    ''' 
    This function applies a sequence of logical solving techniques to attempt solving the Sudoku puzzle. 
    It continuously applies methods such as candidate checking, place finding, twin/triplet elimination, 
    and advanced strategies like X-Wing, checking for errors at each step, until the puzzle is either solved or no further progress can be made. 
    '''
    solving = True
    global error
    global flag_1
    flag_1 = False

    while solving:
        error = False

        # Apply candidate checking
        counter, sudoku_array, sudoku_possible, count, score = candidate_checking(sudoku_array, sudoku_possible, count, score)
        if error:
            return flag_1, error, count, score, sudoku_array, sudoku_possible

        # Repeat candidate checking until no more changes
        while counter > 0:
            counter, sudoku_array, sudoku_possible, count, score = candidate_checking(sudoku_array, sudoku_possible, count, score)
            if error:
                return flag_1, error, count, score, sudoku_array, sudoku_possible
            if counter == 0:
                break

        # Apply place finding by columns
        flag, sudoku_array, sudoku_possible, count, score = place_finding_columns(sudoku_array, sudoku_possible, count, score)
        if error:
            return flag_1, error, count, score, sudoku_array, sudoku_possible

        if flag:
            solving = True
        else:
            # Apply place finding by rows
            flag, sudoku_array, sudoku_possible, count, score = place_finding_rows(sudoku_array, sudoku_possible, count, score)
            if error:
                return flag_1, error, count, score, sudoku_array, sudoku_possible

            if flag:
                solving = True
            else:
                # Apply place finding by minigrids
                flag, sudoku_array, sudoku_possible, count, score = place_finding_minigrids(sudoku_array, sudoku_possible, count, score)
                if error:
                    return flag_1, error, count, score, sudoku_array, sudoku_possible

                if flag:
                    solving = True
                else:
                    # Apply twin elimination in minigrids
                    flag, sudoku_array, sudoku_possible, count, score = twins_in_minigrids(sudoku_array, sudoku_possible, count, score)
                    if error:
                        return flag_1, error, count, score, sudoku_array, sudoku_possible

                    if flag:
                        solving = True
                    else:
                        # Apply twin elimination in rows
                        flag, sudoku_array, sudoku_possible, count, score = twins_in_rows(sudoku_array, sudoku_possible, count, score)
                        if error:
                            return flag_1, error, count, score, sudoku_array, sudoku_possible

                        if flag:
                            solving = True
                        else:
                            # Apply twin elimination in columns
                            flag, sudoku_array, sudoku_possible, count, score = twins_in_columns(sudoku_array, sudoku_possible, count, score)
                            if error:
                                return flag_1, error, count, score, sudoku_array, sudoku_possible

                            if flag:
                                solving = True
                            else:
                                # Apply hidden twins in rows
                                flag, sudoku_array, sudoku_possible, count, score = hidden_twins_in_rows(sudoku_array, sudoku_possible, count, score)
                                if error:
                                    return flag_1, error, count, score, sudoku_array, sudoku_possible

                                if flag:
                                    solving = True
                                else:
                                    # Apply hidden twins in columns
                                    flag, sudoku_array, sudoku_possible, count, score = hidden_twins_in_columns(sudoku_array, sudoku_possible, count, score)
                                    if error:
                                        return flag_1, error, count, score, sudoku_array, sudoku_possible

                                    if flag:
                                        solving = True
                                    else:
                                        # Apply hidden twins in minigrids
                                        flag, sudoku_array, sudoku_possible, count, score = hidden_twins_in_minigrids(sudoku_array, sudoku_possible, count, score)
                                        if error:
                                            return flag_1, error, count, score, sudoku_array, sudoku_possible

                                        if flag:
                                            solving = True
                                        else:
                                            # Apply triplet elimination in minigrids
                                            flag, sudoku_array, sudoku_possible, count, score = triplets_in_minigrids(sudoku_array, sudoku_possible, count, score)
                                            if error:
                                                return flag_1, error, count, score, sudoku_array, sudoku_possible

                                            if flag:
                                                solving = True
                                            else:
                                                # Apply triplet elimination in rows
                                                flag, sudoku_array, sudoku_possible, count, score = triplets_in_rows(sudoku_array, sudoku_possible, count, score)
                                                if error:
                                                    return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                if flag:
                                                    solving = True
                                                else:
                                                    # Apply triplet elimination in columns
                                                    flag, sudoku_array, sudoku_possible, count, score = triplets_in_columns(sudoku_array, sudoku_possible, count, score)
                                                    if error:
                                                        return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                    if flag:
                                                        solving = True
                                                    else:
                                                        # Apply hidden triplets in rows
                                                        flag, sudoku_array, sudoku_possible, count, score = hidden_triplets_in_rows(sudoku_array, sudoku_possible, count, score)
                                                        if error:
                                                            return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                        if flag:
                                                            solving = True
                                                        else:
                                                            # Apply hidden triplets in columns
                                                            flag, sudoku_array, sudoku_possible, count, score = hidden_triplets_in_columns(sudoku_array, sudoku_possible, count, score)
                                                            if error:
                                                                return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                            if flag:
                                                                solving = True
                                                            else:
                                                                # Apply hidden triplets in minigrids
                                                                flag, sudoku_array, sudoku_possible, count, score = hidden_triplets_in_minigrids(sudoku_array, sudoku_possible, count, score)
                                                                if error:
                                                                    return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                if flag:
                                                                    solving = True
                                                                else:
                                                                    # Apply naked quads in rows
                                                                    flag, sudoku_array, sudoku_possible, count, score = naked_quads_in_rows(sudoku_array, sudoku_possible, count, score)
                                                                    if error:
                                                                        return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                    if flag:
                                                                        solving = True
                                                                    else:
                                                                        # Apply naked quads in columns
                                                                        flag, sudoku_array, sudoku_possible, count, score = naked_quads_in_columns(sudoku_array, sudoku_possible, count, score)
                                                                        if error:
                                                                            return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                        if flag:
                                                                            solving = True
                                                                        else:
                                                                            # Apply naked quads in minigrids
                                                                            flag, sudoku_array, sudoku_possible, count, score = naked_quads_in_minigrids(sudoku_array, sudoku_possible, count, score)
                                                                            if error:
                                                                                return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                            if flag:
                                                                                solving = True
                                                                            else:
                                                                                # Apply hidden quads in rows
                                                                                flag, sudoku_array, sudoku_possible, count, score = hidden_quads_in_rows(sudoku_array, sudoku_possible, count, score)
                                                                                if error:
                                                                                    return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                                if flag:
                                                                                    solving = True
                                                                                else:
                                                                                    # Apply hidden quads in columns
                                                                                    flag, sudoku_array, sudoku_possible, count, score = hidden_quads_in_columns(sudoku_array, sudoku_possible, count, score)
                                                                                    if error:
                                                                                        return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                                    if flag:
                                                                                        solving = True
                                                                                    else:
                                                                                        # Apply hidden quads in minigrids
                                                                                        flag, sudoku_array, sudoku_possible, count, score = hidden_quads_in_minigrids(sudoku_array, sudoku_possible, count, score)
                                                                                        if error:
                                                                                            return flag_1, error, count, score, sudoku_array, sudoku_possible

                                                                                        if flag:
                                                                                            solving = True
                                                                                        else:
                                                                                            # Apply X-Wing in rows
                                                                                            flag, sudoku_array, sudoku_possible, count, score = xwing_in_rows(sudoku_array, sudoku_possible, count, score)

                                                                                            if flag:
                                                                                                solving = True
                                                                                            else:
                                                                                                # Apply X-Wing in columns
                                                                                                flag, sudoku_array, sudoku_possible, count, score = xwing_in_columns(sudoku_array, sudoku_possible, count, score)

                                                                                                if flag:
                                                                                                    solving = True
                                                                                                else:
                                                                                                    # Apply X-Wing in minigrids
                                                                                                    flag, sudoku_array, sudoku_possible, count, score = xwing_in_minigrids(sudoku_array, sudoku_possible, count, score)

                                                                                                    if flag:
                                                                                                        solving = True
                                                                                                    else:
                                                                                                        #Final checking to determine if the Sudoku is solved
                                                                                                        flag_1 = final_checking(sudoku_array)
                                                                                                        solving = False

    return flag_1, error, count, score, sudoku_array, sudoku_possible

 
def cells_solved_new(count, count_start): 
    ''' 
    This function calculates how many cells were solved in the current iteration.
    It keeps track of the cumulative total of confirmed values and subtracts it from the current count of solved cells.
    It stores the difference for each iteration in a list.
    '''
    global total 
    for j in range(len(count_list_new)): 
        total = total + count_list_new[j]  # Add up the previously solved counts
    total = total + count_start  # Include the initial count at the start of the solving process
    i = count - total  # Find out how many new cells were solved in this iteration
    count_list_new.append(i)  # Append the result to the list of solved counts
    count = 0 
    total = 0 
    return count_list_new 
