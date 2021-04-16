import pygame
import time
import sys
from typing import List
import random
import numpy as np
pygame.font.init()

# Minesweeper class4
WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Minesweeper")
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GAP_SIZE = 2
font = pygame.font.SysFont('timesnewroman.ttc', 48)


class Square:
    revealed = False
    color = GREY
    mark = False
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.fontsize = 48
        self.font = pygame.font.SysFont('timesnewroman.ttc', self.fontsize)

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
        pygame.draw.rect(WIN, self.color, (self.x + GAP_SIZE, self.y + GAP_SIZE, self.size - GAP_SIZE*2, self.size - GAP_SIZE*2))
        if self.revealed:
            WIN.blit(self.img, (self.x + self.size/2 - 10, self.y + self.size/2 - self.fontsize/4))
        elif self.mark:
            pygame.draw.circle(WIN, RED, (self.x + self.size/2, self.y + self.size/2), 15)


class Board:
    def __init__(self, rows, cols, bombs):
        self.lose = False
        self.win = False
        font = pygame.font.SysFont('timesnewroman.ttc', 200)
        self.lossimg = font.render('YOU LOSE', True, BLACK)
        self.winimg = font.render('YOU WIN', True, BLACK)
        size = WIDTH/rows
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

def findNode(pos, rows):
    x,y = pos
    squareSize = WIDTH/rows
    row = y // squareSize
    col = x // squareSize
    return [row,col]


def update_display(board):
    for row in board.board:
        for square in row:
            square.draw(WIN)
    if board.lose:
        board.draw(WIN)
    if board.win:
        board.draw(WIN)
    pygame.display.update()

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

        

    def playGame(self):

        while True:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.board.lose == False and self.board.win == False:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        [x,y] = findNode(pos, self.rows)
                        x = int(x)
                        y = int(y)
                        clicked = self.board.board[x][y]
                        if clicked.revealed == False:
                            if clicked.reveal() == False:
                                self.board.lose = True
                            self.reveal(x, y)
                            if self.revealedSquares == self.total:
                                self.board.win = True
                    if event.button == 3:
                        pos = pygame.mouse.get_pos()
                        [x,y] = findNode(pos, self.rows)
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
            update_display(self.board)



# mines = Minesweeper()
# mines.main()