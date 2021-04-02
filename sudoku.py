# Sudoku class
import random
import numpy as np
import pygame
import sys

# Needs to fill the board up following Sudoku rules
# Remove a number and check if the board still has just one unique solution
#   Do this using a fact backtracking algorithm
#   If there is now more than one solution, don't remove this number, try another



class Sudoku:
    def __init__(self):
        self.size = 36
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] 

    def printClass(self):
        print("This is the sudoku class.")

    def fillNum(self, num, x, y, board):
        board[x][y] = num
        return board

    # Check if there is just one solution to the board
    def checkNum(self, num, x, y, board):
        solutions = 0

    # Remove a number from the board
    def removeNum(self, num, x, y, board):
        if self.checkRemove(num, x, y, board):
            return self.fillNum(num, x, y, board)
        else:
            num = random.choice(self.numbers)
            locX = random.randint(0, 8)
            locY = random.rantint(0, 8)
            return self.removeNum(num, locX, locY, board)

    def recFill(self, x, y, options, board):
        if not options:
            return
        else:
            row = board[x, :]
            col = board[:, y]
            cell = self.getCell(x, y, board)
            nonOpts = np.union1d(row, col)
            nonOpts = np.union1d(nonOpts, cell) 
            options = np.setdiff1d(self.numbers, nonOpts)
            random.shuffle(options)

        # If board is full return board
        # Else if there are no options, backtrack
        # Else go to the next spot
    
    # Create completely-filled, valid board
    def fillBoard(self, board):
        for x in range(0, 9):
            for y in range(0, 9):
                print("x = ", x)
                print("y = ", y)
                row = board[x, :]   # Get current row
                print(row)
                col = board[:, y]   # Get current col
                print(col)
                # Get the current 3x3 cell that this number is in
                cell = self.getCell(x, y, board)    
                print(cell)
                # The non-options are any numbers that are already in this row or column
                # So the union of the two arrays contains values that are in either row or column
                nonOpts = np.union1d(row, col)
                nonOpts = np.union1d(nonOpts, cell) 
                print(nonOpts)
                options = np.setdiff1d(self.numbers, nonOpts)
                random.shuffle(options)
                print(options)
                for opt in options:
                    if not options:
                        

                board[x][y] = random.choice(options)
                print(board)
            

        return board

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


        board = self.fillBoard(board)

        # Generate all numbers on the board
        # for n in range(0, self.size):
        #     num = random.choice(self.numbers)
        #     locX = random.randint(0, 8)
        #     locY = random.rantint(0, 8)
        #     self.removeNum(num, locX, locY, board)

        return board


        