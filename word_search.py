# Word search class
import random
import numpy as np
import pygame
import copy
import sys


class WordSearch:
    def __init__(self):
        self.size = 17
        self.numberOfWords = 25

        self.letters = ["A", "B", "C", "D", "E", 
                        "F", "G", "H", "I", "J", 
                        "K", "L", "M", "N", "O", 
                        "P", "Q", "R", "S", "T", 
                        "U", "V", "W", "X", "Y", "Z"]

        self.textFile = open("words.txt", "r")
        self.wordsList = self.textFile.read().splitlines()

        self.usedWords = []

        self.directions = ["NW", "N", "NE",
                           "W",        "E", 
                           "SW", "S", "SE"]

    def printClass(self):
        print("This is the word search class.")

    def checkWord(self, word, x, y, dir, board):
        if word in self.usedWords:
            return False

        for i in range(0, len(word)):
            if (dir == "NW" and (board[x-i][y-i] == "-" or board[x-i][y-i] == word[i:i+1]) and 
                x - len(word) > 0 and y - len(word) > 0):
                continue

            elif (dir == "N" and (board[x][y-i] == "-" or board[x][y-i] == word[i:i+1]) and 
                  y - len(word) > 0):
                continue

            elif (dir == "NE" and (board[x+i][y-i] == "-" or board[x+i][y-i] == word[i:i+1]) and 
                  x + len(word) < self.size and y - len(word) > 0):
                continue

            elif (dir == "W" and (board[x-i][y] == "-" or board[x-i][y] == word[i:i+1]) and 
                  x - len(word) > 0):
                continue

            elif (dir == "E" and (board[x+i][y] == "-" or board[x+i][y] == word[i:i+1]) and 
                  x + len(word) < self.size):
                continue

            elif (dir == "SW" and (board[x-i][y+i] == "-" or board[x-i][y+i] == word[i:i+1]) and 
                  x - len(word) > 0 and y+ len(word) < self.size):
                continue

            elif (dir == "S" and (board[x][y+i] == "-" or board[x][y+i] == word[i:i+1]) and 
                  y + len(word) < self.size):
                continue

            elif (dir == "SE" and (board[x+i][y+i] == "-" or board[x+i][y+i] == word[i:i+1]) and 
                  x + len(word) < self.size and y + len(word) < self.size):
                continue

            else:
                return False

        return True

    def fillWord(self, word, x, y, dir, board):
        for i in range(0, len(word)):
            if dir == "NW":
                board[x-i][y-i] = word[i:i+1]

            elif dir == "N":
                board[x][y-i] = word[i:i+1]

            elif dir == "NE":
                board[x+i][y-i] = word[i:i+1]

            elif dir == "W":
                board[x-i][y] = word[i:i+1]

            elif dir == "E":
                board[x+i][y] = word[i:i+1]

            elif dir == "SW":
                board[x-i][y+i] = word[i:i+1]

            elif dir == "S":
                board[x][y+i] = word[i:i+1]

            elif dir == "SE":
                board[x+i][y+i] = word[i:i+1]

        return board

    def addWord(self, word, x, y, dir, board):
        if self.checkWord(word, x, y, dir, board):
            # print(word)
            self.usedWords.append(word)
            return self.fillWord(word, x, y, dir, board)
        else:
            word = random.choice(self.wordsList)
            locX = random.randint(0, self.size - 1)
            locY = random.randint(0, self.size - 1)
            direction = random.choice(self.directions)
            return self.addWord(word, locX, locY, direction, board)

    def generateGame(self):
        board = np.zeros([self.size, self.size], dtype=np.str)

        # Fill the array with -'s as placeholders
        for row in range(0, self.size):
            for col in range(0, self.size):
                board[row][col] = "-"

        # Generate all words on the board
        for n in range(0, self.numberOfWords):
            word = random.choice(self.wordsList)
            locX = random.randint(0, self.size - 1)
            locY = random.randint(0, self.size - 1)
            direction = random.choice(self.directions)
            self.addWord(word, locX, locY, direction, board)

        return board

    def checkSelection(self, board, selected):
        selected.sort()
        tempFor = ""
        tempBack = ""

        for i in selected:
            row = i[1]
            col = i[0]
            if board[row][col] == "-":
                return False
            tempFor += (board[row][col])

        for x in range(0, len(tempFor)):
            tempBack += tempFor[len(tempFor)-x-1]

        if tempFor in self.usedWords:
            return tempFor
        elif tempBack in self.usedWords:
            return tempBack
        else:
            return ""

    def clearSelection(self, selected):
        selected.clear()

    def playGame(self):
        a = self.generateGame()
        board = copy.deepcopy(a)
        # print(board)

        # Pygame initializations
        pygame.init()
        pygame.display.set_caption('Word Search Game')
        scale = 40
        width = 17 * scale
        height = 24 * scale
        twice = scale * 2
        halfW = width // 2
        quarterW = width // 4
        eighthW = width // 8

        running = True
        leftDrag = False
        rightDrag = False
        win = False

        frames = 0
        minutes = 0
        seconds = 0
        total_seconds = 0

        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("consola", 32)
        small_font = pygame.font.SysFont("consola", 28)

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
        letter_color = white
        word_color = white

        check_color = grey
        clear_color = light_blue
        new_color = light_red

        # Selection variables
        selX = -1
        selY = -1
        selected = []

        correct = []
        correctLetters = []

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

                # Events related to left click mouse down
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // scale
                    row = (pos[1] - scale) // scale

                    # Action for letters being selected
                    if (column < self.size and column >= 0) and (row < self.size and row >= 0) and not win:
                        leftDrag = True

                        selX = column
                        selY = row
                        if (selX, selY) not in selected:
                            selected.append((selX, selY))

                    # Action for check word buttton pressed
                    if (pos[0] < quarterW and pos[0] >= 0) and (pos[1] < scale and pos[1] >= 0) and not win:
                        check_color = dark_grey
                        if self.checkSelection(board, selected):
                            correct.append(self.checkSelection(board, selected))
                            for things in selected:
                                correctLetters.append(things)

                        self.clearSelection(selected)

                    # Action for clear word buttton pressed
                    if (pos[0] < halfW and pos[0] >= quarterW) and (pos[1] < scale and pos[1] >= 0) and not win:
                        clear_color = dark_blue
                        self.clearSelection(selected)

                    # Action for new game button; resets all variables, game board, etc.
                    if (pos[0] < quarterW * 3 and pos[0] >= halfW) and (pos[1] < scale and pos[1] >= 0):
                        win = False
                        #score_file = open("high_score.txt", "r")
                        #score = score_file.read().splitlines()   # read in the best time/high score
                        #score_file.close()
                        self.usedWords = []
                        a = self.generateGame()
                        board = copy.deepcopy(a)
                        frames = 0
                        minutes = 0
                        seconds = 0
                        total_seconds = 0
                        selected = []
                        correct = []
                        correctLetters = []
                        new_color = dark_red

                # Events related to left click mouse up
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    leftDrag = False

                # Events related to mouse drag/motion
                elif event.type == pygame.MOUSEMOTION and leftDrag:
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // scale
                    row = (pos[1] - scale) // scale
                    if (column, row) not in selected:
                        selected.append((column, row))

                # Events related to right click mouse down
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // scale
                    row = (pos[1] - scale) // scale

                    # Action for letters being selected
                    if (column < self.size and column >= 0) and (row < self.size and row >= 0):
                        rightDrag = True

                        selX = column
                        selY = row
                        if (selX, selY) in selected:
                            selected.remove((selX, selY))
                
                # Events related to right click mouse up
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    rightDrag = False

                # Events related to mouse drag/motion
                elif event.type == pygame.MOUSEMOTION and rightDrag:
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // scale
                    row = (pos[1] - scale) // scale
                    if (column, row) in selected:
                        selected.remove((column, row))

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

            # Takes the numpy array and puts it into a grid of labels
            for row in range(0, self.size):
                for col in range(0, self.size):
                    if (col, row) in selected:
                        letter_color = light_yellow
                    elif (col, row) in correctLetters:
                        letter_color = light_green
                    else:
                        letter_color = white

                    if a[row][col] == "-":
                        a[row][col] = random.choice(self.letters)

                    half = scale // 2
                    letter = font.render(a[row][col], True, black, letter_color)
                    letterRect = letter.get_rect()
                    letterRect.center = (col * scale + half, row * scale + (scale + half))
                    pygame.draw.rect(screen, letter_color, [scale * col, scale * row + scale, scale, scale])
                    screen.blit(letter, letterRect)

            # Display all the words at the bottom of the screen
            for i in range(0, self.numberOfWords):
                col = i % 5
                row = i // 5

                if self.usedWords[i] in correct:
                    word_color = light_green
                else:
                    word_color = white

                fifth = width // 5
                centerFifth = fifth // 2
                half = scale // 2
                word = small_font.render(self.usedWords[i], True, black, word_color)
                wordRect = word.get_rect()
                wordRect.center = (col * fifth + centerFifth, (row * scale + half) + (18 * scale))
                pygame.draw.rect(screen, word_color, [fifth * col, (scale * row) + (18 * scale), fifth, scale])
                screen.blit(word, wordRect)

            # Check word and clear buttons
            check = small_font.render("CHECK WORD", True, black, check_color)
            checkRect = check.get_rect()
            checkRect.center = (eighthW, half)
            pygame.draw.rect(screen, check_color, [0, 0, quarterW, scale])
            screen.blit(check, checkRect)

            clear = small_font.render("CLEAR", True, black, clear_color)
            clearRect = clear.get_rect()
            clearRect.center = (3 * (eighthW), half)
            pygame.draw.rect(screen, clear_color, [quarterW, 0, halfW, scale])
            screen.blit(clear, clearRect)

            # New game button and timer
            new = small_font.render("NEW GAME", True, black, new_color)
            newRect = new.get_rect()
            newRect.center = (5 * (eighthW), half)
            pygame.draw.rect(screen, new_color, [halfW, 0, quarterW * 3, scale])
            screen.blit(new, newRect)
            
            timer = small_font.render(time, True, black, light_orange)
            timerRect = timer.get_rect()
            timerRect.center = (7 * (eighthW), half)
            pygame.draw.rect(screen, light_orange, [quarterW * 3, 0, width, scale])
            screen.blit(timer, timerRect)

            # Back to menu button
            menu = small_font.render("BACK TO MENU", True, black, light_purple)
            menuRect = menu.get_rect()
            menuRect.center = (width // 2, (23 * scale) + (scale // 2))
            pygame.draw.rect(screen, light_purple, [0, 23 * scale, width, height])
            screen.blit(menu, menuRect)

            # Win condition
            if len(correct) == self.numberOfWords:
                win = True
                text = "{0:02}:{1:02}".format(int(score[0]), int(score[1]))
                #print(score)
                if int(score[0]) > minutes or (int(score[0]) >= minutes and int(score[1]) > seconds):
                    #score_file = open("high_score.txt", "w")
                    #score = [str(minutes), str(seconds)]
                    with open("high_score.txt", "w") as out:
                        out.write("{}\n{}".format(str(minutes), str(seconds)))
                    #score_file.writelines(score)
                    text = "{0:02}:{1:02}".format(minutes, seconds)
                    score_file.close()

                complete = font.render("Puzzle complete! Best time: " + text, True, black, light_orange)
                completeRect = complete.get_rect()
                completeRect.center = (7 * (eighthW), half)
                pygame.draw.rect(screen, light_orange, [quarterW * 3, 0, width, scale])
                screen.blit(complete, completeRect)

            frames += 1
            clock.tick(60)

            pygame.display.update()
        
        pygame.quit()

# test = WordSearch()
# test.playGame()