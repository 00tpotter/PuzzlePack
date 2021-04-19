import pygame
import time
import sys
from typing import List
import random
import numpy as np
pygame.font.init()

# Minesweeper class4
WIDTH = 800

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
PURPLE = (255, 175, 255)
LIGHT_RED = (255, 175, 175)
ORANGE = (255, 200, 145)

GAP_SIZE = 1
SCALE = 40
font = pygame.font.SysFont('timesnewroman.ttc', 42)
small_font = pygame.font.SysFont('consola', 32)


class Square:
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.fontsize = 42
        self.font = pygame.font.SysFont('timesnewroman.ttc', self.fontsize)
        self.revealed = False
        self.color = GREY
        self.mark = False

    def setValue(self, n):
        self.value = n
        self.img = font.render(str(self.value), True, BLACK)
    def getValue(self):
        return self.value
    def reveal(self):
        self.revealed = True
        self.color = WHITE
        if self.value == -1:
            return False
        return True
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x + GAP_SIZE, self.y + GAP_SIZE + SCALE, self.size - GAP_SIZE*2, self.size - GAP_SIZE*2))
        if self.revealed:
            WIN.blit(self.img, (self.x + self.size/2 - 7, (self.y + self.size/2 - 13) + SCALE))
        elif self.mark:
            pygame.draw.circle(WIN, RED, (self.x + self.size/2, self.y + self.size/2 + SCALE), 15)


class Board:
    def __init__(self, rows, cols, bombs):
        self.lose = False
        self.win = False
        font = pygame.font.SysFont('timesnewroman.ttc', 150)
        self.lossimg = font.render('YOU LOSE', True, BLACK)
        self.winimg = font.render('YOU WIN', True, BLACK)
        size = WIDTH//rows
        self.board: List[List[Square]] = [[Square(j*size, i*size, size) for j in range(cols)] for i in range(rows)]
        numSquares = rows*cols
        self.cols = cols
        self.rows = rows
        rand = np.zeros((1, numSquares - bombs))
        rand = np.concatenate((rand, -1 * np.ones((1, bombs))), axis = None)
        random.shuffle(rand)
        rand = rand.astype(int)
        for i in range(len(rand)):
            row = int(i / rows)
            col = i % cols
            self.board[row][col].setValue(rand[i])

    def setSquares(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if (self.board[x][y].getValue() != -1):
                    self.board[x][y].setValue(self.checkBombs(x,y))

    def checkBombs(self, x, y):
        value = 0
        for i in range(-1,2):

            if(x == 0 and i == -1): continue #Boundry Case
            elif (x == self.cols - 1 and i == 1): continue #Boundry Case

            for j in range(-1,2):

                if(y == 0 and j == -1): continue #Boundry Case
                elif(y == self.rows - 1 and j == 1): continue #Boundry Case

                if (i == 0 and j ==0): continue #Bomb Tile
                elif(self.board[x+i][y+j].getValue() == -1): 
                    value += 1
        return value
    
    def printBoard(self):
        for List in self.board:
            for Square in List:
                print(Square.getValue() , end = "")
                print(", " , end = "")
            print()

    def getSquare(self, x, y):
        return self.board[x][y]

    def draw(self, WIN):
        if self.lose:
            WIN.blit(self.lossimg, (150, WIDTH/2 -100))
        elif self.win:
            WIN.blit(self.winimg, (150, WIDTH/2 -100))



class Minesweeper:
    numFlags = 0
    revealedSquares = 0
    def __init__(self):
        #rows = int(input("How many rows? "))
        rows = 20
        self.rows = rows
        cols = rows
        #bombs = int(input("How many bombs? "))
        self.bombs = 60
        self.total = rows*cols - self.bombs
        self.board = Board(rows, cols, self.bombs)
        self.board.setSquares()

    def reveal(self, x, y): # take in clicked tile as parameter
        self.revealedSquares += 1
        curr = self.board.getSquare(x,y)
        if(curr.getValue() != 0):
            curr.reveal()
            return

        curr.reveal()
        for i in range(-1,2):
            if(x + i < 0):continue #Boundry Case
            elif (x + i == self.board.rows): continue #Boundry Case
            for j in range(-1,2):
                if(y + j < 0):continue #Boundry Case
                elif (y + j  == self.board.cols): continue #Boundry Case

                curr = self.board.getSquare(x + i, y + j)
                if(curr.revealed):
                    continue
                self.reveal(x + i, y + j)


    def findNode(self, pos, rows):
        x,y = pos
        squareSize = WIDTH//rows
        row = (y - SCALE) // squareSize
        col = x // squareSize
        return [row,col]


    def update_display(self, board, WIN):
        for row in board.board:
            for square in row:
                square.draw(WIN)
        if board.lose:
            board.draw(WIN)
        if board.win:
            board.draw(WIN)
        pygame.display.update() 

    def playGame(self):
        score_file = open("ms_high_score.txt", "r")
        score = score_file.read().splitlines()      # read in the best time/high score
        score_file.close()
        
        HEIGHT = WIDTH + (SCALE * 2)
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        frames = 0
        minutes = 0
        seconds = 0
        total_seconds = 0
        clock = pygame.time.Clock()
        running = True
        
        while running:
            if not self.board.lose and not self.board.win:
                total_seconds = frames // 60
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time = "{0:02}:{1:02}".format(minutes, seconds)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    tempCol = pos[0] // SCALE
                    tempRow = (pos[1] - SCALE) // SCALE
                    
                    if event.button == 1:
                        if (tempCol < 20 and tempCol >= 0) and (tempRow < 20 and tempRow >= 0):
                            [x,y] = self.findNode(pos, self.rows)
                            x = int(x)
                            y = int(y)
                            clicked = self.board.board[x][y]
                            if clicked.revealed == False and self.board.lose == False and self.board.win == False:
                                if clicked.reveal() == False:
                                    self.board.lose = True
                                self.reveal(x, y)
                                if self.revealedSquares == self.total:
                                    self.board.win = True

                        if (pos[0] < WIDTH // 2 and pos[0] >= 0) and (pos[1] < SCALE and pos[1] >= 0):
                            self.numFlags = 0
                            self.revealedSquares = 0
                            rows = 20
                            self.rows = rows
                            cols = rows
                            self.cols = rows
                            self.bombs = 60
                            self.total = rows*cols - self.bombs
                            self.board = Board(rows, cols, self.bombs)
                            self.board.setSquares()
                            frames = 0
                            minutes = 0
                            seconds = 0
                            total_seconds = 0

                        if (pos[0] < WIDTH and pos[0] >= 0) and (pos[1] < HEIGHT and pos[1] >= 21 * SCALE):
                            running = False
                    
                    if event.button == 3 and self.board.lose == False and self.board.win == False:
                        [x,y] = self.findNode(pos, self.rows)
                        x = int(x)
                        y = int(y)
                        clicked = self.board.board[x][y]
                        if clicked.revealed == False:
                            if clicked.mark == False and self.numFlags < self.bombs:
                                clicked.mark = True
                                self.numFlags += 1
                            elif clicked.mark:
                                clicked.mark = False
                                self.numFlags -= 1

                # Visual change for buttons being clicked
                else:
                    pygame.display.update()

                    frames += 1
                    clock.tick(60)

            # Buttons
            # New game button
            new = small_font.render("NEW GAME", True, BLACK, LIGHT_RED)
            newRect = new.get_rect()
            newRect.center = (WIDTH // 4, SCALE // 2)
            pygame.draw.rect(WIN, LIGHT_RED, [0, 0, WIDTH // 2, SCALE])
            WIN.blit(new, newRect)

            # Timer
            timer = small_font.render(time, True, BLACK, ORANGE)
            timerRect = timer.get_rect()
            timerRect.center = (3 * (WIDTH // 4), SCALE // 2)
            pygame.draw.rect(WIN, ORANGE, [WIDTH // 2, 0, WIDTH // 2, SCALE])
            WIN.blit(timer, timerRect)

            # Back to menu button
            menu = small_font.render("BACK TO MENU", True, BLACK, PURPLE)
            menuRect = menu.get_rect()
            menuRect.center = (WIDTH // 2, (21 * SCALE) + (SCALE // 2))
            pygame.draw.rect(WIN, PURPLE, [0, 21 * SCALE, WIDTH, SCALE])
            WIN.blit(menu, menuRect)

            if self.board.win:
                text = "{0:02}:{1:02}".format(int(score[0]), int(score[1]))
            
                if int(score[0]) > minutes or (int(score[0]) >= minutes and int(score[1]) > seconds):
                    with open("ms_high_score.txt", "w") as out:
                        out.write("{}\n{}".format(str(minutes), str(seconds)))
                    text = "{0:02}:{1:02}".format(minutes, seconds)
                    score_file.close()
            
                time = "Puzzle complete! Best time: " + text
            
            frames += 1
            clock.tick(60)
            pygame.display.update()
            self.update_display(self.board, WIN)
            
