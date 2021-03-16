# Word search class
import random
import numpy as np

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
            print(word)
            self.usedWords.append(word)
            return self.fillWord(word, x, y, dir, board)
        else:
            word = random.choice(self.wordsList)
            locX = random.randint(0, self.size - 1)
            locY = random.randint(0, self.size - 1)
            direction = random.choice(self.directions)
            return self.addWord(word, locX, locY, direction, board)

    def generateGame(self):
        board = np.zeros([self.size, self.size], dtype = np.str)

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

    def checkSelection(self):
        return

    def clearSelection(self):
        return