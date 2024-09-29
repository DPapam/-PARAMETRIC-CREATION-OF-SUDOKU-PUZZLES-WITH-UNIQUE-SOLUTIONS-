#________This file includes the graphic part of the application________# 
import pygame 
from generation import * 
import time 
from pygame.locals import * 
import os, re 
import random 
from sys import exit 
 
pygame.font.init()       
pygame.init() 


#_________Class Sudoku represents the sudoku grid_________# 
class Sudoku: 
    """
    Represents the Sudoku grid and manages the logic for interacting with the grid, 
    placing numbers, handling user input, and drawing the cells.
    """
    def __init__(self, rows, cols, width, height, backup_sudoku, first_sudoku): 
        """
        Initializes the Sudoku grid with given dimensions, board state, and solution.
        """
        self.rows = rows 
        self.cols = cols 
        self.board = backup_sudoku  # The current puzzle state
        self.right = first_sudoku  # The solved version of the puzzle
        self.cubes = [Cell(backup_sudoku[i], i // 9 , i % 9, i, width, height) for i in range(rows * cols)]  # Create Cell objects for each position
        self.width = width 
        self.height = height 
        self.model = backup_sudoku  # Keep track of the grid model
        self.selected = None  # No cell is selected at initialization
        self.hint_selected = False  # Hint feature is inactive


    # Refreshes the Sudoku grid model to reflect the current state of the cubes
    def update_model(self):                                                                                   
        self.model = [self.cubes[i].value for i in range(self.rows * self.cols)]    # Model array includes the values of cubes


    # Places a value into the selected cell, verifying if it's correct
    def place(self, val):                                                                                            
        cell = self.selected         
        if self.cubes[cell].value == 0:                                                                        # If the cell is empty  
            self.cubes[cell].set(val) 
            self.update_model() 
            if self.model[cell] == self.right[cell]:                                                         # If the value is the right one 
                return True                                                                                              # Return True 
            else: 
                self.cubes[cell].set(0)                                                                             # Else return False 
                self.cubes[cell].set_temp(0) 
                self.update_model() 
                return False 


    # Temporarily places a value in the selected cell before confirmation
    def sketch(self, val):                                                                                          
        cell = self.selected 
        self.cubes[cell].set_temp(val) 


    # Draws the Sudoku grid, cells, and any hints on the game window
    def draw(self, win):                                                                                            
        gap = self.width / 9 
        for i in range(self.rows + 1):                
            if i % 3 == 0 : 
                thick = 4 
            else: 
                thick = 1 
            pygame.draw.line(win, (32, 88, 103), (0, i * gap), (self.width, i * gap), thick) 
            pygame.draw.line(win, (32, 88, 103), (i * gap, 0), (i * gap, self.height), thick) 
        if self.hint_selected == True:                                                                          # Draw hint button 
            pygame.draw.rect(win, (204, 0, 102), (40 + 540, 270 - 20, 80 ,40), 4)
        for i in range(self.rows * self.cols):                                                               # Draw Cells 
            self.cubes[i].draw(win, 32, 88, 103) 


    # Selects a specific cell in the grid
    def select(self, cell): 
        for i in range(self.rows * self.cols):                                                            # Reset all other cells 
            if i != cell: 
                self.cubes[i].selected = False 
            else: 
                self.cubes[i].selected = True 
        self.hint_selected = False                                                                               # Reset Hint     
        self.selected = cell  


    # Selects a random empty cell to display its correct value as a hint
    def select_hint(self, empty):                                                                              
        cell = random.choice(empty) 
        while self.board[cell] != 0: 
            cell = random.choice(empty) 
        self.cubes[cell].set(self.right[cell]) 
        self.hint_selected = True 
        self.update_model()
    

    # Clears the value of the selected cell
    def clear(self):                                                                                                     
        cell = self.selected 
        if self.cubes[cell].value == 0: 
            self.cubes[cell].set_temp(0) 


    # Handles mouse click events and determines which cell or button was clicked
    def click(self, pos):                                                                                              
        hint = False
        new = False
        menu = False
 
        if pos[0] < self.width and pos[1] < self.height:                                             # The user selects a cell 
            gap = self.width / 9 
            x = pos[0] // gap 
            y = pos[1] // gap 
            cell = y * 9 + x 
            cell = int(cell) 
            return (cell, hint, new, menu) 
        else:                                                                                                                  # The user selects the hint button 
            if pos[0] < 660 and pos[0] > 580: 
                if pos[1] > 250 and pos[1] < 290: 
                    hint = True 
                    cell = None 
                elif pos[1] > 200 and pos[1] < 240:
                    new = True
                    cell = None
                elif pos[1] > 300 and pos[1] < 340:
                    menu = True
                    cell = None
                cell = None
                return (cell, hint, new, menu)
            cell = None                                                                                                     # The user selects nothing 
            hint = False
            new = False
            menu = False
            return (cell, hint, new, menu)


    # Checks if the user clicked the menu button
    def click_menu(self, pos):
        if pos[0] < 390 and pos[0] > 310: 
            if pos[1] > 500 and pos[1] < 540:  
                return True
        return False


    # Checks if the puzzle is completely solved
    def finish(self):                                                                                                     
        for i in range(self.rows * self.cols): 
            if self.cubes[i].value == 0: 
                return False 
        return True 


    # Identifies the row, column, and subgrid based on the selected cell
    def important_cells(self, cell):
        """
        Identify the row, column, and subgrid related to the selected cell.
        Returns a set of indices representing all related cells.
        """
        row = cell // 9
        col = cell % 9
        
        # Cells in the same row and column
        important_cells = [r * 9 + col for r in range(9)] + [row * 9 + c for c in range(9)]
        
        # Cells in the same 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                important_cells.append(r * 9 + c)
        
        return set(important_cells)  # Return as a set to avoid duplicates


    # Highlights the important cells (same row, column, and subgrid) for the selected cell
    def draw_important(self, win):
        if self.selected is not None:
            important = self.important_cells(self.selected)
        else:
            important = set()
        
        light_blue = (173, 216, 230)
        gap = self.width / 9

        for i in important:
            row = i // 9
            col = i % 9
            x = col * gap
            y = row * gap
            pygame.draw.rect(win, light_blue, (x, y, gap, gap))  # Fill the background with light blue


#_________Class Cell represents every cell of the grid_________# 
class Cell: 
    """
    Represents each cell in the Sudoku grid. Handles value placement and drawing.
    """
    rows = 9 
    cols = 9 

    # Initializes each cell with its value, position, and other attributes
    def __init__(self, value, row, col, i, width, height): 
        self.value = value  # Actual value of the cell
        self.temp = 0  # Temporary value (if user has not confirmed)
        self.row = row  # Row position of the cell
        self.col = col  # Column position of the cell
        self.cell = i  # Index of the cell in the grid
        self.width = width
        self.height = height
        self.selected = False  # If the cell is currently selected


    # Draws the value (permanent or temporary) in the cell
    def draw(self, win, r, g, b): 
        fnt = pygame.font.SysFont("Footlight MT Light", 40)  
        gap = self.width / 9 
        x = self.col * gap 
        y = self.row * gap 
        if self.temp != 0 and self.value == 0:  # If the user has sketched a value
            text = fnt.render(str(self.temp), 1, (128, 128, 128))  # Light color for sketch
            win.blit(text, (x + 5, y + 5))  # Display sketch in the corner
        elif self.value != 0:  # Confirmed value
            text = fnt.render(str(self.value), 1, (r, g, b))  # Display in cell center
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))  
        if self.selected:  # Highlight selected cell
            pygame.draw.rect(win, (204, 0, 102), (x, y, gap, gap), 4)  


    # Sets the permanent value of the cell
    def set(self, val):                                                                                                
        self.value = val 


    # Sets the temporary value of the cell
    def set_temp(self, val):                                                                                 
        self.temp = val 


#_________Function to redraw the game window_________# 
def redraw_window(win, board, time, wrong): 
    """
    Redraws the entire game window including the Sudoku board, timer, mistakes, 
    and buttons like 'Hint' and 'New'.
    """
    win.fill((242, 220, 218))  # Background color of the window
    fnt = pygame.font.SysFont("Footlight MT Light", 40) 
    
    # Draw the current playing time
    text = fnt.render("Time: " + calculate_time(time), 1, (32, 88, 103))  
    win.blit(text, (700 - 160, 560)) 
    
    # Draw the number of mistakes
    text = fnt.render("X " * wrong, 1, (204, 0, 102))  
    win.blit(text, (20, 560)) 
    
    # Draw the hint button
    text = fnt.render("Hint", 1, (204, 0, 102))  
    win.blit(text, (50 + 540, 270 - 12)) 
    pygame.draw.rect(win, (32, 88, 103), (40 + 540, 270 - 20, 80 ,40), 4) 
    
    # Draw the new game button
    text = fnt.render("New", 1, (204, 0, 102))  
    win.blit(text, (50 + 540, 220 - 12))
    pygame.draw.rect(win, (32, 88, 103), (40 + 540, 220 - 20, 80, 40), 4)
    
    # Draw the menu button
    fnt = pygame.font.SysFont("Footlight MT Light", 38)
    text = fnt.render("Menu", 1, (204, 0, 102))  
    win.blit(text, (45 + 540, 320 - 12)) 
    pygame.draw.rect(win, (32, 88, 103), (40 + 540, 320 - 20, 80, 40), 4)

    board.draw_important(win)
    board.draw(win)  # Draw board


#_________Function to calculate playtime_________# 
def calculate_time(secs): 
    """
    Calculates the playtime in minutes and seconds based on the total seconds passed.
    """
    sec = secs % 60 
    minute = secs // 60 
    hour = minute // 60 

    mat = " " + str(minute) + ":" + str(sec) 
    return mat 


#_______Define the size of the window and load required images_________#  
display_width = 700 
display_height = 600 
global win 
BLACK = (0, 0, 0) 
win = pygame.display.set_mode((display_width, display_height)) 
pygame.display.set_caption("Sudoku") 

# Load images for various screens and game elements
start_screen = pygame.image.load(os.path.join('pictures',"startmenu.png")).convert() 
start_screen = pygame.transform.smoothscale(start_screen, (display_width, display_height)) 
start_screen = start_screen.convert(start_screen) 

block_image1 = pygame.image.load(os.path.join('pictures',"block1.png")).convert() 
block_image1 = pygame.transform.smoothscale(block_image1, (185, 62)) 
block_image1 = block_image1.convert(block_image1) 
block_image1.set_colorkey(BLACK) 

block_image = pygame.image.load(os.path.join('pictures',"block.png")).convert() 
block_image = pygame.transform.smoothscale(block_image, (185, 95)) 
block_image = block_image.convert(block_image) 
block_image.set_colorkey(BLACK) 

wait_image = pygame.image.load(os.path.join('pictures',"wait.png")).convert() 
wait_image = pygame.transform.smoothscale(wait_image, (display_width, display_height)) 
wait_image = wait_image.convert(wait_image) 

gameover_screen = pygame.image.load(os.path.join('pictures',"gameover.png")).convert() 
gameover_screen = pygame.transform.smoothscale(gameover_screen, (display_width, display_height)) 
gameover_screen = gameover_screen.convert(gameover_screen) 

win_screen = pygame.image.load(os.path.join('pictures',"won.png")).convert() 
win_screen = pygame.transform.smoothscale(win_screen, (display_width, display_height)) 
win_screen = win_screen.convert(gameover_screen) 


#_________Function to display the start menu_________# 
def start_menu(): 
    """
    Displays the start menu screen where the user can select the difficulty level.
    """
    win.blit(start_screen,(0, 0)) 
      
#_________Class Game handles the main game loop and menu navigation_________# 
class Game: 
    """
    Manages the main game loop, including menu navigation, difficulty selection, 
    and game generation.
    """
    
    # Shows the background with the start menu and lets the user select difficulty level
    def background(self): 
        run = True 
        while run: 
            start_menu()  # Display the start menu screen
            for event in pygame.event.get(): 
                if event.type == QUIT:  # Handle quit event
                    pygame.quit() 
                    exit() 
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                    pos = pygame.mouse.get_pos() 
                    x = pos[0] 
                    y = pos[1] 
                    if 258.25 < x < 441.85 and 225 < y < 283.75: 
                        print("Easy") 
                        difficulty = 1 
                        run = False  
                    elif 258.25 < x < 441.85 and 301.246 < y < 359.996: 
                        print("Medium") 
                        difficulty = 2 
                        run = False 
                    elif 258.25 < x < 441.85 and 380 < y < 438.75: 
                        print("Difficult") 
                        difficulty = 3 
                        run = False 
                    elif 258.25 < x < 441.85 and 460 < y < 549.39: 
                        print("Extremely Difficult") 
                        difficulty = 4 
                        run = False
                    else:
                        continue
                    return difficulty  # Return the selected difficulty level       
            pygame.display.update() 


    # Generates the Sudoku puzzle based on the user's selected difficulty
    def start_to_generate(self, user_option):
        """
        Generates the puzzle based on the difficulty level selected by the user.
        """
        if user_option == 1: 
            win.blit(block_image1, (258.25, 224))  # Click the button 
            pygame.display.update() 
            number = random.randrange(40, 46) 
            givens = 4 
        elif user_option == 2: 
            win.blit(block_image1, (258.25, 299.5)) 
            pygame.display.update() 
            number = random.randrange(46, 50) 
            givens = 3 
        elif user_option == 3: 
            win.blit(block_image1, (258.25, 377)) 
            pygame.display.update() 
            number = random.randrange(50, 54) 
            givens = 2 
        elif user_option == 4: 
            win.blit(block_image, (258.25, 455)) 
            pygame.display.update() 
            number = random.randrange(54, 58)
            givens = 0 
        win.blit(wait_image, (0, 0))  # Wait image appears 
        pygame.display.update() 
        for event in pygame.event.get():  # If the user wants to close the window 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                exit()

        start_time = time.perf_counter()        
        backup_sudoku, first_sudoku = generation(number, user_option, givens)  # Create Sudoku puzzle 
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.5f} seconds")

        self.main(backup_sudoku, first_sudoku, user_option)  # Call the main game function  


    # Plays background music and proceeds to puzzle generation based on user input
    def next_step(self): 
        run = True 
        while run: 
            pygame.mixer.music.load('Mirage.wav')  # Play background music 
            pygame.mixer.music.set_volume(0.05) 
            pygame.mixer.music.play(-1) 
            user_option = self.background()  # Get the selected difficulty 
            self.start_to_generate(user_option)  # Start generating the puzzle
            run = False


    # Detects the next action in the game (e.g., navigating to the main menu)
    def next_action(self, board):
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse clicks 
                    pos = pygame.mouse.get_pos()
                    menu = board.click_menu(pos)  # Check if the menu button was clicked
                    if menu == True:
                        self.next_step()  # Navigate to the menu


    # Main game loop that handles the logic, drawing, and interactions during the game
    def main(self, backup_sudoku, first_sudoku, user_option):  
        board = Sudoku(9, 9, 540, 540, backup_sudoku, first_sudoku)  # Initialize the board
        key = None 
        run = True 
        start = time.time() 
        wrong = 0 
        win_flag = True 
        while run: 
            play_time = round(time.time() - start) 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    exit() 

                # Handle key presses for number input and clearing cells
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_1:  key = 1 
                    if event.key == pygame.K_2:  key = 2 
                    if event.key == pygame.K_3:  key = 3 
                    if event.key == pygame.K_4:  key = 4 
                    if event.key == pygame.K_5:  key = 5 
                    if event.key == pygame.K_6:  key = 6 
                    if event.key == pygame.K_7:  key = 7 
                    if event.key == pygame.K_8:  key = 8 
                    if event.key == pygame.K_9:  key = 9 
                    if event.key == pygame.K_DELETE:  # If the user presses Delete 
                        board.clear()  # Clear the cell value 
                        key = None 
                    if event.key == pygame.K_RETURN:  # If the user presses Enter 
                        cell = board.selected  # Check if the value confirms the cell  
                        if board.cubes[cell].temp != 0:  
                            if not board.place(board.cubes[cell].temp):  # If the choice is not right  
                                wrong += 1  # Increment mistakes 
                                if wrong == 3: 
                                    win_flag = False 
                                    run = False 
                            key = None 

                            if board.finish():  # Check if the board is solved 
                                win_flag = True 
                                run = False 

                # Handle mouse clicks for selecting cells and buttons
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    pos = pygame.mouse.get_pos()  # Get the coordinates 
                    clicked, hint, new, menu = board.click(pos) 
                    if clicked != None:  # The user clicked a cell 
                        if hint == False and new == False and menu == False:  
                            board.select(clicked)
                            board.draw_important(win)
                            key = None 
                    else:     
                        if hint == True:  # The user selects hint button  
                            empty = empty_function(board.model) 
                            board.select_hint(empty) 
                            key = None 
                        elif new == True:
                            key = None
                            self.start_to_generate(user_option)
                        elif menu == True:
                            key = None
                            self.next_step()
                        if board.finish(): 
                            run = False 

            if board.selected != None and key != None:  # If a value is confirmed  
                board.sketch(key)  # Call sketch function  

            redraw_window(win, board, play_time, wrong)  # Redraw window with updated data 
            pygame.display.update() 

        # Handle game over or victory scenarios
        if wrong == 3:  # Defeat 
            win.blit(gameover_screen, (0, 0))  # Display game over screen 
            # Draw centered "Menu" button near the bottom
            button_width = 80
            button_height = 40
            button_x = (display_width / 2) - (button_width / 2)
            button_y = display_height - 100

            fnt = pygame.font.SysFont("Footlight MT Light", 38)
            text = fnt.render("Menu", 1, (204, 0, 102))
            win.blit(text, (button_x + (button_width / 2 - text.get_width() / 2), button_y + (button_height / 2 - text.get_height() / 2)))
            pygame.draw.rect(win, (32, 88, 103), (button_x, button_y, button_width, button_height), 4)
            pygame.display.update() 
            self.next_action(board)

        if win_flag == True:  # Victory 
            win.blit(win_screen, (0, 0))  # Display win screen 
            # Draw centered "Menu" button near the bottom
            button_width = 80
            button_height = 40
            button_x = (display_width / 2) - (button_width / 2)
            button_y = display_height - 100

            fnt = pygame.font.SysFont("Footlight MT Light", 38)
            text = fnt.render("Menu", 1, (204, 0, 102))
            win.blit(text, (button_x + (button_width / 2 - text.get_width() / 2), button_y + (button_height / 2 - text.get_height() / 2)))
            pygame.draw.rect(win, (32, 88, 103), (button_x, button_y, button_width, button_height), 4)
            pygame.display.update() 
            self.next_action(board)


# Initialize and start the game
game = Game()  # Game variable takes all the attributes and functions of Game Class 
game.next_step()  # The first called function is next_step 


# Event loop to keep the game running until the user quits
while True:  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit()
