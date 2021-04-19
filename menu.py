# Menu class
import word_search
#import chess
import sudoku
import minesweeper
import pygame

class Menu:    
    def __init__(self):
        self.ws_game = word_search.WordSearch()
        #self.chess_game = chess.Chess()
        self.sudoku_game = sudoku.Sudoku()
        self.ms_game = minesweeper.Minesweeper()

    def printClass(self):
        print("This is the menu class.")
        #self.ws_game.printClass()
        #self.chess_game.printClass()
        #self.sudoku_game.printClass()
        #self.ms_game.printClass()

    def playWordSearch(self):
        self.ws_game.playGame()  

    def playSudoku(self):
        self.sudoku_game.playGame()

    def playMinesweeper(self):
        self.ms_game.playGame()
        

    def chooseGame(self):
        # Pygame initializations
        pygame.init()
        pygame.display.set_caption('Puzzle Pack')
        scale = 50
        width = scale * 15
        height = scale * 10
        twiceS = scale * 2
        halfS = scale // 2
        quarterS = scale // 4
        halfW = width // 2
        quarterW = width // 4
        eighthW = width // 8
        quartH = height // 4
        eighthH = height // 8

        running = True
        frames = 0

        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("lato", 32)
        small_font = pygame.font.SysFont("lato", 24)

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

        # Color effects for each button
        playSud = False
        sudText = white
        sudBack = black
        sudBorder = 0

        playWord = False
        wordText = white
        wordBack = black
        wordBorder = 0

        playMine = False
        mineText = white
        mineBack = black
        mineBorder = 0

        playCh = False
        chText = white
        chBack = black
        chBorder = 0


        textColor = white
        backColor = black
        border = 0

        image = pygame.image.load("PuzzlePack1.png")
        # image = pygame.transform.scale(image, (400, 400))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()

                    x = pos[0]
                    y = pos[1]

                    # Sudoku button pressed
                    if (x <= scale * 14 and x >= scale * 10) and (y >= scale + quarterS and y <= scale * 3 - quarterS):
                        sudText = black
                        sudBack = white
                        sudBorder = 2
                        playSud = True
                        

                    # Word Search button pressed
                    if (x <= scale * 14 and x >= scale * 10) and (y >= scale * 3 + quarterS and y <= scale * 5 - quarterS):
                        wordText = black
                        wordBack = white
                        wordBorder = 2
                        playWord = True

                    # Minesweeper button pressed
                    if (x <= scale * 14 and x >= scale * 10) and (y >= scale * 5 + quarterS and y <= scale * 7 - quarterS):
                        mineText = black
                        mineBack = white
                        mineBorder = 2
                        playMine = True

                    # Chess button pressed
                    if (x <= scale * 14 and x >= scale * 10) and (y >= scale * 7 + quarterS and y <= scale * 9 - quarterS):
                        chText = black
                        chBack = white
                        chBorder = 2
                        playCh = True

                # Reset visual changes in button clicks
                else:
                    sudText = white
                    sudBack = black
                    sudBorder = 0
                    if playSud:
                        self.playSudoku()
                        pygame.display.set_caption('Puzzle Pack')
                        screen = pygame.display.set_mode((width, height))
                    playSud = False

                    wordText = white
                    wordBack = black
                    wordBorder = 0
                    if playWord:
                        self.playWordSearch()
                        pygame.display.set_caption('Puzzle Pack')
                        screen = pygame.display.set_mode((width, height))
                    playWord = False

                    mineText = white
                    mineBack = black
                    mineBorder = 0
                    if playMine:
                        self.playMinesweeper()
                        pygame.display.set_caption('Puzzle Pack')
                        screen = pygame.display.set_mode((width, height))
                    playMine = False

                    chText = white
                    chBack = black
                    chBorder = 0
                    
                    frames += 1
                    clock.tick(60)
                    pygame.display.update()

            # Displaying everything on the screen
            screen.fill(white)
            
            screen.blit(image, (0, 0))

            # Sudoku button
            sud = font.render("SUDOKU", True, sudText, sudBack)
            sudRect = sud.get_rect()
            sudRect.center = (scale * 12, scale * 2)
            pygame.draw.rect(screen, black, [scale * 10, scale + quarterS, scale * 4, scale * 2 - halfS], sudBorder)
            screen.blit(sud, sudRect)

            # Word search button
            word = font.render("WORD SEARCH", True, wordText, wordBack)
            wordRect = word.get_rect()
            wordRect.center = (scale * 12, scale * 4)
            pygame.draw.rect(screen, black, [scale * 10, scale * 3 + quarterS, scale * 4, scale * 2 - halfS], wordBorder)
            screen.blit(word, wordRect)

            # Minesweeper button
            mine = font.render("MINESWEEPER", True, mineText, mineBack)
            mineRect = mine.get_rect()
            mineRect.center = (scale * 12, scale * 6)
            pygame.draw.rect(screen, black, [scale * 10, scale * 5 + quarterS, scale * 4, scale * 2 - halfS], mineBorder)
            screen.blit(mine, mineRect)

            # Chess puzzle button
            ch = font.render("CHESS", True, chText, chBack)
            chRect = ch.get_rect()
            chRect.center = (scale * 12, scale * 8)
            pygame.draw.rect(screen, black, [scale * 10, scale * 7 + quarterS, scale * 4, scale * 2 - halfS], chBorder)
            screen.blit(ch, chRect)

            frames += 1
            clock.tick(60)
            pygame.display.update()
        
        #pygame.display.update()
        pygame.quit()

game = Menu()
game.chooseGame()
