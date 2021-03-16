# Menu class
import word_search
import chess
import sudoku
import minesweeper

import pygame
import sys

class Menu:    
    def __init__(self):
        self.ws_game = word_search.WordSearch()
        self.chess_game = chess.Chess()
        self.sudoku_game = sudoku.Sudoku()
        self.ms_game = minesweeper.Minesweeper()

    def printClass(self):
        print("This is the menu class.")
        self.ws_game.printClass()
        self.chess_game.printClass()
        self.sudoku_game.printClass()
        self.ms_game.printClass()

    def playWordSearch(self):
        newBoard = self.ws_game.generateGame()
        print(newBoard)

        # Pygame code
        pygame.init()
        pygame.display.set_caption('Word Search Game')
        width = 720
        height = 960

        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("consola", 28)

        running = True
        frames = 0

        while(running):
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            frames += 1
            clock.tick(60)

        pygame.quit()

game = Menu()
game.printClass()
game.playWordSearch()