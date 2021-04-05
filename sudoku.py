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

    def printClass(self):
        print("This is the sudoku class.")

    # def fillNum(self, x, y, board):
    #     board[x][y] = 0
    #     return board

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
                    print("hewwo")
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
            #print(board)
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

        solution = copy.deepcopy(board)

        optBoard = np.zeros([9, 9], dtype=object)
        optBoard = self.getOptBoard(board, optBoard)
        # for row in range(0, 9):
        #     for col in range(0, 9):
        #         print(optBoard[row][col])

        # locX = random.randint(0, 8)
        # locY = random.randint(0, 8)
        # self.removeNum(locX, locY, board, optBoard)

        for i in range(0, 45):
            locX = random.randint(0, 8)
            locY = random.randint(0, 8)
            self.removeNum(locX, locY, board, optBoard)

        return board
