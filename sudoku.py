# Sudoku class
import random
import numpy as np
import pygame
import sys


class Sudoku:
    def __init__(self):
        self.size = 36
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] 

    def printClass(self):
        print("This is the sudoku class.")

    def fillNum(self, num, x, y, board):
        board[x][y] = num
        return board

    # This is going to be the hard function to make
    # It needs to check the whole board and determine if the placement is valid
    def checkNum(self, num, x, y, board):


    def addNum(self, num, x, y, board):
        if self.checkNum(num, x, y, board):
            return self.fillNum(num, x, y, board)
        else:
            num = random.choice(self.numbers)
            locX = random.randint(0, 8)
            locY = random.rantint(0, 8)
            return self.addNum(num, locX, locY, board)
   
    def generateGame(self):
        board = np.zeros([9, 9], dtype=np.str)

        # Fill the array with -'s as placeholders
        for row in range(0, 9):
            for col in range(0, 9):
                board[row][col] = "-"

        # Generate all numbers on the board
        for n in range(0, self.size):
            num = random.choice(self.numbers)
            locX = random.randint(0, 8)
            locY = random.rantint(0, 8)
            self.addNum(num, locX, locY, board)

        return board


        