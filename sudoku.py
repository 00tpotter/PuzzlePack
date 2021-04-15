# Sudoku class
import random
import numpy as np
import pygame
import copy
import sys

# Needs to fill the board up following Sudoku rules
# Remove a number and check if the board still has just one unique solution
#   Do this using a fact backtracking algorithm
#   If there is now more than one solution, don't remove this number, try another

class Sudoku:
    def __init__(self):
        self.size = 36
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.solutions = 0
        self.answer = np.zeros([9, 9], dtype=np.int32)

    def printClass(self):
        return "This is the Sudoku class."

    # Check if there is just one solution to the board
    def checkRemove(self, board, optBoard):        
        if self.solutions > 1:
            return False

        if np.all(num > 0 for num in board):
            #print(board)
            self.solutions += 1
        
        optBoard = self.getOptBoard(board, optBoard)
        lowPair = self.findLowOpt(optBoard)
        x, y = lowPair
        options = optBoard[x][y]

        for nums in options:
            if len(options) > 0:
                board[x][y] = num
                sys.setrecursionlimit(2600)
                if self.checkRemove(board, optBoard):
                    return True
                board[x][y] = 0

        if self.solutions == 1:
            return True
        
        return False

    # Remove a number from the board
    def removeNum(self, x, y, board, optBoard):
        board[x][y] = 0
        self.solutions = 0
        if self.checkRemove(board, optBoard):
            return board
        else:
            locX = random.randint(0, 8)
            locY = random.randint(0, 8)
            return self.removeNum(locX, locY, board, optBoard)

    # Recursive backtracking algorithm to fill the board all the way
    # following sudoku rules
    def fillBoard(self, x, y, board):
        if y >= 9 and x < 8:
            x += 1
            y = 0
        if x >= 8 and y >= 9:
            return True

        options = self.getOpts(x, y, board)
        random.shuffle(options)

        for num in options:
            if len(options) > 0:
                board[x][y] = num
                sys.setrecursionlimit(2600)
                if self.fillBoard(x, y+1, board):
                    return True
                board[x][y] = 0
        return False
    
    def getOpts(self, x, y, board):
        row = board[x, :]
        col = board[:, y]
        cell = self.getCell(x, y, board)
        nonOpts = np.union1d(row, col)
        nonOpts = np.union1d(nonOpts, cell) 
        options = np.setdiff1d(self.numbers, nonOpts)

        return options
    
    def getOptBoard(self, board, optBoard):
        for x in range(0, 9):
            for y in range(0, 9):
                optBoard[x][y] = self.getOpts(x, y, board)

        return optBoard

    def findLowOpt(self, optBoard):
        row = -1
        col = -1
        lowest = 9
        lowPair = (row, col)
        for x in range(0, 9):
            for y in range(0, 9):
                if len(optBoard[x][y]) < lowest:
                    lowest = len(optBoard[x][y])
                    lowPair = (x, y)

        return lowPair

    def getCell(self, x, y, board):
        cell = np.zeros([0], dtype=np.int32)
        # Cell 1
        if(x >= 0 and x <= 2 and y >= 0 and y <= 2):
            cell = np.concatenate((cell, board[0, 0:3]))
            cell = np.concatenate((cell, board[1, 0:3]))
            cell = np.concatenate((cell, board[2, 0:3]))
        # Cell 2
        elif(x >= 3 and x <= 5 and y >= 0 and y <= 2):
            cell = np.concatenate((cell, board[3, 0:3]))
            cell = np.concatenate((cell, board[4, 0:3]))
            cell = np.concatenate((cell, board[5, 0:3]))
        # Cell 3
        elif(x >= 6 and x <= 8 and y >= 0 and y <= 2):
            cell = np.concatenate((cell, board[6, 0:3]))
            cell = np.concatenate((cell, board[7, 0:3]))
            cell = np.concatenate((cell, board[8, 0:3]))
        # Cell 4
        elif(x >= 0 and x <= 2 and y >= 3 and y <= 5):
            cell = np.concatenate((cell, board[0, 3:6]))
            cell = np.concatenate((cell, board[1, 3:6]))
            cell = np.concatenate((cell, board[2, 3:6]))
        # Cell 5
        elif(x >= 3 and x <= 5 and y >= 3 and y <= 5):
            cell = np.concatenate((cell, board[3, 3:6]))
            cell = np.concatenate((cell, board[4, 3:6]))
            cell = np.concatenate((cell, board[5, 3:6]))
        # Cell 6
        elif(x >= 6 and x <= 8 and y >= 3 and y <= 5):
            cell = np.concatenate((cell, board[6, 3:6]))
            cell = np.concatenate((cell, board[7, 3:6]))
            cell = np.concatenate((cell, board[8, 3:6]))
        # Cell 7
        elif(x >= 0 and x <= 2 and y >= 6 and y <= 8):
            cell = np.concatenate((cell, board[0, 6:9]))
            cell = np.concatenate((cell, board[1, 6:9]))
            cell = np.concatenate((cell, board[2, 6:9]))
        # Cell 8
        elif(x >= 3 and x <= 5 and y >= 6 and y <= 8):
            cell = np.concatenate((cell, board[3, 6:9]))
            cell = np.concatenate((cell, board[4, 6:9]))
            cell = np.concatenate((cell, board[5, 6:9]))
        # Cell 9
        elif(x >= 6 and x <= 8 and y >= 6 and y <= 8):
            cell = np.concatenate((cell, board[6, 6:9]))
            cell = np.concatenate((cell, board[7, 6:9]))
            cell = np.concatenate((cell, board[8, 6:9]))
        
        return cell
   
   # Set up the board and begin the algorithm
    def generateGame(self):
        board = np.zeros([9, 9], dtype=np.int32)

        # Fill the array with -'s as placeholders
        for row in range(0, 9):
            for col in range(0, 9):
                board[row][col] = 0

        x = 0
        y = 0
        self.fillBoard(x, y, board)
        print(board)

        self.answer = copy.deepcopy(board)

        optBoard = np.zeros([9, 9], dtype=object)
        optBoard = self.getOptBoard(board, optBoard)

        for i in range(0, 45):
            locX = random.randint(0, 8)
            locY = random.randint(0, 8)
            self.removeNum(locX, locY, board, optBoard)

        return board

    def playGame(self):
        board = self.generateGame()
        temp = copy.deepcopy(board)

        # Pygame initializations
        pygame.init()
        pygame.display.set_caption('Sudoku Game')
        scale = 50
        width = scale * 9
        height = scale * 11
        twiceS = scale * 2
        halfS = scale // 2
        halfW = width // 2
        quarterW = width // 4
        eighthW = width // 8

        running = True
        win = False

        frames = 0
        minutes = 0
        seconds = 0
        total_seconds = 0

        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("consola", 40)
        small_font = pygame.font.SysFont("consola", 22)


        # Colors
        white = (255, 255, 255)
        grey = (200, 200, 200)
        dark_grey = (175, 175, 175)
        black = (0, 0, 0)

        light_red = (255, 175, 175)
        dark_red = (230, 150, 150)
        light_orange = (255, 200, 145)
        light_yellow = (255, 255, 200)
        light_green = (200, 255, 200)
        light_blue = (200, 200, 255)
        dark_blue = (175, 175, 230)
        light_purple = (255, 175, 255)
        light_pink = (255, 200, 200)
        light_brown = (200, 150, 100)

        # Default colors
        number_color = white
        select_color = grey

        check_color = grey
        clear_color = light_blue
        new_color = light_red

        # Textbox input
        active = False
        text = ""
        selX = -1
        selY = -1
        selected = (selX, selY)
        checked = False

        while(running):
            # Variables for calculating time
            if not win:
                total_seconds = frames // 60
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time = "{0:02}:{1:02}".format(minutes, seconds)

            # Actions/events from input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // scale
                    row = (pos[1] - scale) // scale

                    selY = column
                    selX = row

                    # Action for numbers being selected
                    if (column < 9 and column >= 0) and (row < 9 and row >= 0) and not win and board[selX][selY] == 0:
                        active = True
                        if (selX, selY) != selected:
                            selected = (selX, selY)
                        else:
                            selected = (-1, -1)
                    else:
                        active = False
                        selected = (-1, -1)

                    # Action for check numbers buttton pressed
                    if (pos[0] < quarterW and pos[0] >= 0) and (pos[1] < scale and pos[1] >= 0) and not win:
                        check_color = dark_grey
                        checked = True
                        # if np.array_equal(temp, self.answer):
                        #     number_color = light_green
                        # else:
                        #     number_color = light_red

                        selected = (-1, -1)

                    # Action for clear all buttton pressed
                    if (pos[0] < halfW and pos[0] >= quarterW) and (pos[1] < scale and pos[1] >= 0) and not win:
                        clear_color = dark_blue
                        temp = copy.deepcopy(board)
                        checked = False

                    # Action for new game button; resets all variables, game board, etc.
                    if (pos[0] < quarterW * 3 and pos[0] >= halfW) and (pos[1] < scale and pos[1] >= 0):
                        win = False
                        board = self.generateGame()
                        temp = copy.deepcopy(board)
                        frames = 0
                        minutes = 0
                        seconds = 0
                        total_seconds = 0
                        selected = (-1, -1)
                        active = False
                        text = ""
                        new_color = dark_red
                        checked = False

                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text = event.unicode
                            if board[selX][selY] == 0:
                                temp[selX][selY] = int(text)
                                text = ""
                                active = False
                                selected = (-1, -1)

                # Visual change for buttons being clicked
                else:
                    check_color = grey
                    clear_color = light_blue
                    new_color = light_red

                    pygame.display.update()

                    frames += 1
                    clock.tick(60)

            # Displaying everything on the screen
            screen.fill(white)

            # Display the board
            for row in range(0, 9):
                for col in range(0, 9):
                    if (row, col) == selected:
                        number_color = light_yellow
                    elif checked:
                        if temp[row][col] == self.answer[row][col]:
                            number_color = light_green
                        else:
                            number_color = light_red
                    elif temp[row][col] != 0 and board[row][col] == 0:
                        number_color = select_color
                    else:
                        number_color = white
                    num = str(temp[row][col])
                    if temp[row][col] == 0:
                        num = " "
                    number = font.render(num, True, black, number_color)
                    numberRect = number.get_rect()
                    numberRect.center = (col * scale + halfS, row * scale + (scale + halfS))
                    pygame.draw.rect(screen, number_color, [scale * col, scale * row + scale, scale, scale])
                    screen.blit(number, numberRect)

                    # Box borders
                    pygame.draw.rect(screen, black, [scale * col, scale * row + scale, scale, scale], width=1)

            # 3x3 cell borders
            pygame.draw.rect(screen, black, [(scale * 3), scale-1, (scale * 3)+1, (scale * 9)+1], width=2)
            pygame.draw.rect(screen, black, [0-1, (scale * 4), (scale * 9)+1, (scale * 3)+1], width=2)

            # Check word and clear buttons
            check = small_font.render("CHECK ANSWER", True, black, check_color)
            checkRect = check.get_rect()
            checkRect.center = (eighthW, halfS)
            pygame.draw.rect(screen, check_color, [0, 0, quarterW, scale])
            screen.blit(check, checkRect)

            clear = small_font.render("CLEAR ALL", True, black, clear_color)
            clearRect = clear.get_rect()
            clearRect.center = (3 * (eighthW), halfS)
            pygame.draw.rect(screen, clear_color, [quarterW, 0, halfW, scale])
            screen.blit(clear, clearRect)

            # New game button and timer
            new = small_font.render("NEW GAME", True, black, new_color)
            newRect = new.get_rect()
            newRect.center = (5 * (eighthW), halfS)
            pygame.draw.rect(screen, new_color, [halfW, 0, quarterW * 3, scale])
            screen.blit(new, newRect)
            
            timer = small_font.render(time, True, black, light_orange)
            timerRect = timer.get_rect()
            timerRect.center = (7 * (eighthW), halfS)
            pygame.draw.rect(screen, light_orange, [quarterW * 3, 0, width, scale])
            screen.blit(timer, timerRect)

            # Back to menu button
            menu = small_font.render("BACK TO MENU", True, black, light_purple)
            menuRect = menu.get_rect()
            menuRect.center = (width // 2, (10 * scale) + (scale // 2))
            pygame.draw.rect(screen, light_purple, [0, 10 * scale, width, height])
            screen.blit(menu, menuRect)


            frames += 1
            clock.tick(60)

            pygame.display.update()

        pygame.quit()