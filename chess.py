# Chess class
import pygame
import time
import sys
import random
import numpy as np
from typing import List
pygame.font.init()

WIDTH = 800
squareSize = WIDTH / 8

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 200)
BLUE = (50, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (255, 175, 255)
LIGHT_RED = (255, 175, 175)
ORANGE = (255, 200, 145)

SCALE = 50

font = pygame.font.SysFont('timesnewroman.ttc', 48)
small_font = pygame.font.SysFont('consola', 32)

##piece class, passed in a single number from 0 to 13, representing the different pieces.
# None = 0
# King = 1
# Pawn = 2
# Knight = 3
# Bishop = 4
# Rook = 5
# Queen = 6

# The above is for white pieces, for black pieces of the same type add 7.
class Piece:
    type = 0
    side = 0
    moved = False
    enPassant = False
    def __init__(self, type):
        self.type = type
        
        if type > 6:
            self.type = type - 7
            self.side = 1 
        str = "chessImages/"
        if self.side == 0:
            str += "white"
        else:
            str += "black"
        if self.type == 1:
            str += "King.png"
        elif self.type == 2:
            str += "Pawn.png"
        elif self.type == 3:
            str += "Knight.png"
        elif self.type == 4:
            str += "Bishop.png"
        elif self.type == 5:
            str += "Rook.png"
        elif self.type == 6:
            str += "Queen.png"
        self.image = pygame.image.load(str)
        self.image = pygame.transform.scale(self.image, (100, 100))

    def isKing(self):
        return type == 1

    def isPawn(self):
        return type == 2

    def isKnight(self):
        return type == 3

    def isBishop(self):
        return type == 4

    def isRook(self):
        return type == 5

    def isQueen(self):
        return type == 6

    def whichSide(self):
        return self.side

    def hasMoved(self):
        return self.moved

    def toString(self):
        out = ""
        if self.side == 0:
            out += "w"
        else:
            out += "b"
        if self.type == 1:
            out += "k"
        elif self.type == 2:
            out += "p"
        elif self.type == 3:
            out += "n"
        elif self.type == 4:
            out += "b"
        elif self.type == 5:
            out += "r"
        elif self.type == 6:
            out += "q"
        else:
            out = "bug"
        return out

def squareToIndex(stringMove):
    num1 = -1
    num2 = -1
    p = stringMove[0]
    if p == 'a':
        num1 = 1
    if p == 'b':
            num1 = 2
    if p == 'c':
        num1 = 3
    if p == 'd':
        num1 = 4
    if p == 'e':
        num1 = 5
    if p == 'f':
        num1 = 6
    if p == 'g':
        num1 = 7
    if p == 'h':
        num1 = 8
    num2 = (8 - int(stringMove[1])) * 8 - 1
    return num2 + num1

def loadPuzzles():
    text = open("cpuzzles.txt", "r")
    lines = [line.split(',') for line in text]
    return lines

class Square:
    occupiedBy = None
    def __init__(self, index):
        self.row = int(index / 8)
        self.col = int(index % 8)
        self.y = int(self.row * squareSize)
        self.x = int(self.col * squareSize)
        if (self.row + self.col) % 2 == 0:
            self.color = WHITE
        else:
            self.color = BLACK
        self.hasPiece = False
        self.highlighted = False

    def highlight(self):
        self.highlighted = True

    def unhighlight(self):
        self.highlighted = False
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y + SCALE, squareSize, squareSize))
        if self.hasPiece:
            WIN.blit(self.occupiedBy.image, (self.x, self.y + SCALE))
        if self.highlighted:
            pygame.draw.circle(WIN, GREY, (self.x + squareSize/2, self.y + squareSize/2 + SCALE), 15)

    def placePiece(self, Piece):
        self.occupiedBy = Piece
        self.hasPiece = True

    def movePiece(self):
        self.occupiedBy = None
        self.hasPiece = False

class Board:
    board: List[Square] = [Square(i) for i in range(64)]

    def printBoard(self):
        for square in self.board:
            if square.hasPiece == False:
                print("[  ]", end = '')
            else:
                print("[", square.occupiedBy.toString(), "]", sep = '', end = '')
            if (square.col == 7):
                print()

    def positionFromFen(self, fen):
        pos = 0
        first = fen.index(" ")
        second = fen.index(" ", first + 1)
        third = fen.index(" ", second + 1)
        fourth = fen.index(" ", third + 1)
        turn = 0
        C1 = False
        C2 = False
        C3 = False
        C4 = False
        enPassant = -1
        for i in range(first):
            x = fen[i]
            if (x.isdigit()):
                pos += int(x)
            elif (x == '/'):
                continue
            elif (x == 'p'):
                self.board[pos].placePiece(Piece(9))
                pos = pos + 1
            elif (x == 'k'):
                self.board[pos].placePiece(Piece(8))
                pos = pos + 1
            elif (x == 'q'):
                self.board[pos].placePiece(Piece(13))
                pos = pos + 1
            elif (x == 'b'):
                self.board[pos].placePiece(Piece(11))
                pos = pos + 1
            elif (x == 'n'):
                self.board[pos].placePiece(Piece(10))
                pos = pos + 1
            elif (x == 'r'):
                self.board[pos].placePiece(Piece(12))
                pos = pos + 1
            elif (x == 'P'):
                self.board[pos].placePiece(Piece(2))
                pos = pos + 1
            elif (x == 'K'):
                self.board[pos].placePiece(Piece(1))
                pos = pos + 1
            elif (x == 'R'):
                self.board[pos].placePiece(Piece(5))
                pos = pos + 1
            elif (x == 'Q'):
                self.board[pos].placePiece(Piece(6))
                pos = pos + 1
            elif (x == 'B'):
                self.board[pos].placePiece(Piece(4))
                pos = pos + 1
            elif (x == 'N'):
                self.board[pos].placePiece(Piece(3))
                pos = pos + 1
            else:
                print("invalid FEN")
                pygame.quit()
                sys.exit()

        if fen[first + 1] == 'b':
            turn = 1

        for i in range(second+1, third):
            if fen[i] == 'K':
                C1 = True
            if fen[i] == 'Q':
                C2 = True
            if fen[i] == 'k':
                C3 = True
            if fen[i] == 'q':
                C4 = True
        
        num1 = -1
        num2 = -1
        if fen[third + 1] != '-':
            p = fen[third + 1]
            if p == 'a':
                num1 = 1
            if p == 'b':
                num1 = 2
            if p == 'c':
                num1 = 3
            if p == 'd':
                num1 = 4
            if p == 'e':
                num1 = 5
            if p == 'f':
                num1 = 6
            if p == 'g':
                num1 = 7
            if p == 'h':
                num1 = 8
            num2 = (8 - int(fen[third + 2])) * 8 - 1
            enPassant = num1 + num2
        return [turn, C1, C2, C3, C4, enPassant]      


class Chess:
    def selectPiece(self, B, index):
        piece = B.board[index].occupiedBy
        if piece.type == 2:
            if piece.side == 0:
                return self.pawn_moves_w(B, index)
            else:
                return self.pawn_moves_b(B, index)
        elif piece.type == 1:
            return self.king_moves(B, index)
        elif piece.type == 3:
            return self.knight_moves(B, index)
        elif piece.type == 4:
            return self.bishop_moves(B, index)
        elif piece.type == 5:
            return self.rook_moves(B, index)
        elif piece.type == 6:
            return self.queen_moves(B, index)

    def pawn_moves_w(self, B, index):
        moves = []
        if index >= 8:
            if B.board[index - 8].hasPiece == False:
                moves.append(index - 8)
                if index >= 16:
                    if (B.board[index - 16].hasPiece == False and int(index / 8) == 6):
                        moves.append(index - 16)
        if index >= 7:  
            if B.board[index-7].hasPiece:
                if B.board[index - 7].occupiedBy.side == 1:
                    moves.append(index - 7)
        if index >= 9:
            if B.board[index-9].hasPiece:
                if B.board[index - 9].occupiedBy.side == 1:
                    moves.append(index - 9)
        if (index < 31 and index > 23):
            if B.board[index + 1].hasPiece:
                if B.board[index + 1].occupiedBy.side == 1 and B.board[index + 1].occupiedBy.enPassant:
                    moves.append(index - 7)
        if (index < 32 and index > 24):
            if B.board[index - 1].hasPiece:
                if B.board[index - 1].occupiedBy.side == 1 and B.board[index - 1].occupiedBy.enPassant:
                    moves.append(index - 9)

        return moves

    def pawn_moves_b(self, B, index):
        moves = []
        if index <= 55:
            if B.board[index + 8].hasPiece == False:
                moves.append(index + 8)
                if index <= 47:
                    if (B.board[index + 16].hasPiece == False and int(index / 8) == 1):
                        moves.append(index + 16)
        if index <= 56:
            if B.board[index+7].hasPiece:
                if B.board[index + 7].occupiedBy.side == 0:
                    moves.append(index + 7)
        if index <= 54:
            if B.board[index+9].hasPiece:
                if B.board[index + 9].occupiedBy.side == 0:
                    moves.append(index + 9)
        if (index < 39 and index > 31):
            if B.board[index + 1].hasPiece:
                if B.board[index + 1].occupiedBy.side == 0 and B.board[index + 1].occupiedBy.enPassant:
                    moves.append(index + 9)
        if (index < 40 and index > 32):
            if B.board[index - 1].hasPiece:
                if B.board[index - 1].occupiedBy.side == 0 and B.board[index - 1].occupiedBy.enPassant:
                    moves.append(index + 7)

        return moves

    def knight_moves(self, B, index):
        moves = []
        
        side = B.board[index].occupiedBy.side
        i = int(index / 8)
        j = index % 8

        for x in range(-2, 3):
            for y in range(-2, 3):
                if x ** 2 + y ** 2 == 5:
                    if self.on_board((x + i, y + j)):
                        if B.board[index + 8*x + y].hasPiece == False:
                            moves.append(index + x*8 + y)
                        elif B.board[index + 8*x + y].occupiedBy.side != side:
                            moves.append(index + x*8 + y)
        return moves

    def bishop_moves(self, B, index):
        moves = []
        side = B.board[index].occupiedBy.side
        i = int(index / 8)
        j = index % 8
        diagonals = [[[i + x, j + x] for x in range(1, 8)],
                    [[i + x, j - x] for x in range(1, 8)],
                    [[i - x, j + x] for x in range(1, 8)],
                    [[i - x, j - x] for x in range(1, 8)]]
        
        for direction in diagonals:
            for position in direction:
                if self.on_board(position):
                    posIndex = position[0] * 8 + position[1]
                    if B.board[posIndex].hasPiece == False:
                        moves.append(posIndex)
                    elif B.board[posIndex].occupiedBy.side != side:
                        moves.append(posIndex)
                        break
                    else:
                        break

        return moves

    def rook_moves(self, B, index):
        moves = []
        side = B.board[index].occupiedBy.side
        i = int(index / 8)
        j = index % 8
        columns = [[[i + x, j] for x in range(1, 8 - i)],
                [[i - x, j] for x in range(1, 1 + i)],
                [[i, j + x] for x in range(1, 8 - j)],
                [[i, j - x] for x in range(1, 1 + j)]]
        
        for direction in columns:
            for position in direction:
                if self.on_board(position):
                    posIndex = position[0] * 8 + position[1]
                    if B.board[posIndex].hasPiece == False:
                        moves.append(posIndex)
                    elif B.board[posIndex].occupiedBy.side != side:
                        moves.append(posIndex)
                        break
                    else:
                        break

        return moves

    def queen_moves(self, B, index):
        m1 = self.bishop_moves(B, index)
        m2 = self.rook_moves(B, index)
        for i in m2:
            m1.append(i)
        return m1

    def king_moves(self, B, index):
        moves = []
        side = B.board[index].occupiedBy.side
        i = int(index / 8)
        j = index % 8
        pairs = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], 
                [i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
        for position in pairs:
            if self.on_board(position):
                posIndex = position[0] * 8 + position[1]
                if B.board[posIndex].hasPiece == False:
                    moves.append(posIndex)
                elif B.board[posIndex].occupiedBy.side != side:
                    moves.append(posIndex)
        king = B.board[index].occupiedBy
        if king.side == 0:
            if king.hasMoved() == False and B.board[63].hasPiece:
                if B.board[61].hasPiece == False and B.board[62].hasPiece == False and B.board[63].occupiedBy.hasMoved() == False:
                    moves.append(62)
            if king.hasMoved() == False and B.board[56].hasPiece:
                if B.board[59].hasPiece == False and B.board[58].hasPiece == False and B.board[57].hasPiece == False and B.board[56].occupiedBy.hasMoved() == False:
                    moves.append(58)
        if king.side == 1:
            if king.hasMoved() == False and B.board[7].hasPiece:
                if B.board[5].hasPiece == False and B.board[6].hasPiece == False and B.board[7].occupiedBy.hasMoved() == False:
                    moves.append(6)
            if king.hasMoved() == False and B.board[0].hasPiece:
                if B.board[3].hasPiece == False and B.board[2].hasPiece == False and B.board[1].hasPiece == False and B.board[0].occupiedBy.hasMoved() == False:
                    moves.append(2)
        
        return moves

    def on_board(self, position):
        if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
            return False
        return True

    def highlight_squares(self, B, moves):
        for i in moves:
            B.board[i].highlight()

    def unhighlight_squares(self, B, moves):
        for i in moves:
            B.board[i].unhighlight()

    def update_display(self, win, Board, score, winIn):
        for square in Board.board:
            square.draw(win)
        text1 = font.render("Score: " + str(score), True, RED)
        text2 = font.render("Find mate in " + str(winIn), True, RED)
        rect1 = text1.get_rect()
        rect1.center = (200, 25)
        rect2 = text2.get_rect()
        rect2.center = (600, 25)
        win.blit(text1, rect1)
        win.blit(text2, rect2)

        # Buttons
        # New game button
        new = small_font.render("NEW GAME", True, BLACK, LIGHT_RED)
        newRect = new.get_rect()
        newRect.center = (WIDTH // 6, SCALE // 2)
        pygame.draw.rect(win, LIGHT_RED, [0, 0, WIDTH // 3, SCALE])
        win.blit(new, newRect)

        # Timer
        timer = small_font.render("Score: " + str(score), True, BLACK, ORANGE)
        timerRect = timer.get_rect()
        timerRect.center = (3 * (WIDTH // 6), SCALE // 2)
        pygame.draw.rect(win, ORANGE, [WIDTH // 3, 0, WIDTH // 3, SCALE])
        win.blit(timer, timerRect)

        # Mate in
        mate = small_font.render("Mate in: " + str(winIn), True, BLACK, YELLOW)
        mateRect = mate.get_rect()
        mateRect.center = (5 * (WIDTH // 6), SCALE // 2)
        pygame.draw.rect(win, YELLOW, [2 * (WIDTH // 3), 0, WIDTH // 3, SCALE])
        win.blit(mate, mateRect)

        # Back to menu button
        menu = small_font.render("BACK TO MENU", True, BLACK, PURPLE)
        menuRect = menu.get_rect()
        menuRect.center = (WIDTH // 2, (17 * SCALE) + (SCALE // 2))
        pygame.draw.rect(win, PURPLE, [0, 17 * SCALE, WIDTH, SCALE])
        win.blit(menu, menuRect)

        pygame.display.update()

    def findNode(self, pos):
        x,y = pos
        row = (y - SCALE) // squareSize
        col = x // squareSize
        return int(row)*8 + int(col)

    def playGame(self):
        score_file = open("chess_high_score.txt", "r")
        score = score_file.read().splitlines()      # read in the best time/high score
        score_file.close()

        pygame.init()
        WIN = pygame.display.set_mode((WIDTH,WIDTH + (SCALE*2)))
        pygame.display.set_caption("Chess")
        B = Board()
        counter = -1
        puzzles = loadPuzzles()
        temp1 = list(range(0, 19))
        temp2 = list(range(20,39))
        temp3 = list(range(40,59))
        random.shuffle(temp1)
        random.shuffle(temp2)
        random.shuffle(temp3)
        temp = temp1[0:10] + temp2[0:10] + temp3[0:10]
                      
        for puzzleNum in temp:
            winIn = 3
            if counter < 9:
                winIn = 2
            counter += 1
            for sq in B.board:
                sq.movePiece()
            fen = puzzles[puzzleNum][0]
            [t, c1, c2, c3, c4, ep] = B.positionFromFen(fen)
            if (c1 == False):
                if B.board[63].hasPiece:
                    B.board[63].occupiedBy.moved = True
            if (c2 == False):
                if B.board[56].hasPiece:
                    B.board[56].occupiedBy.moved = True
            if (c3 == False):
                if B.board[7].hasPiece:
                    B.board[7].occupiedBy.moved = True
            if (c4 == False):
                if B.board[0].hasPiece:
                    B.board[0].occupiedBy.moved = True
            if ep != -1:
                B.board[ep].occupiedBy.enPassant = True
            # B.printBoard()
            
            moveNum = t
            correct = True
            moves = []
            selected = False
            selectedSquare = -1


            moveList = puzzles[puzzleNum][1:]
            for move in range(len(moveList)):

                computerMove = False
                if move % 2 == 1:
                    computerMove = True
                wholeMove = moveList[move]
                move1 = wholeMove[0:2]
                move2 = wholeMove[2:4]
                m1 = squareToIndex(move1)
                m2 = squareToIndex(move2)
                moveNotMade = True

                while moveNotMade:
                    pygame.time.delay(25)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if computerMove:
                            pygame.time.delay(500)
                            moves = self.selectPiece(B, m1)
                            self.highlight_squares(B, moves)
                            self.update_display(WIN, B, counter, winIn)
                            pygame.time.delay(500)
                            piece = B.board[m1].occupiedBy
                            B.board[m2].placePiece(piece)
                            B.board[m1].movePiece()
                            self.unhighlight_squares(B, moves)
                            self.update_display(WIN, B, counter, winIn)
                            moveNotMade = False
                            moveNum += 1
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            
                            tempCol = pos[0] // squareSize
                            tempRow = (pos[1] - SCALE) // squareSize

                            if (tempCol < 8 and tempCol >= 0) and (tempRow < 8 and tempRow >= 0):
                                sq = self.findNode(pos)
                            
                                if selected == False:
                                    if B.board[sq].hasPiece:
                                        piece = B.board[sq].occupiedBy
                                        if (piece.side == moveNum % 2):
                                            moves = self.selectPiece(B, sq)
                                            self.highlight_squares(B, moves)
                                            selectedSquare = sq
                                            selected = True
                                        else:
                                            print("It is not your turn!")
                                    else:
                                        print("No piece here")
                                else:
                                    choseMove = False
                                    for i in moves:
                                        if i == sq:
                                            piece = B.board[selectedSquare].occupiedBy
                                            if sq != m2 or selectedSquare != m1:
                                                print("game over!")
                                                moveNotMade = False
                                                correct = False
                                                break
                                            if piece.type == 2:
                                                if (abs(selectedSquare - sq) == 16):
                                                    piece.enPassant = True
                                                elif abs(selectedSquare - sq) != 8:
                                                    if B.board[sq].hasPiece == False:
                                                        if piece.side == 0:
                                                            B.board[sq + 8].occupiedBy = None
                                                            B.board[sq + 8].hasPiece = False
                                                        else:
                                                            B.board[sq - 8].occupiedBy = None
                                                            B.board[sq - 8].hasPiece = False
                                            if piece.type == 1:
                                                if (selectedSquare - sq == -2):
                                                    rook = B.board[selectedSquare + 3].occupiedBy
                                                    B.board[selectedSquare + 1].placePiece(rook)
                                                    B.board[selectedSquare + 3].movePiece()
                                                if (selectedSquare - sq == 2):
                                                    rook = B.board[selectedSquare - 4].occupiedBy
                                                    B.board[selectedSquare - 1].placePiece(rook)
                                                    B.board[selectedSquare - 4].movePiece()

                                            B.board[sq].placePiece(piece)
                                            B.board[selectedSquare].movePiece()
                                            selectedSquare = -1
                                            selected = False
                                            self.unhighlight_squares(B, moves)
                                            moves = []
                                            moveNum += 1
                                            moveNotMade = False
                                            choseMove = True
                                            piece.moved = True
                                            for s in B.board:
                                                if s.occupiedBy != None:
                                                    if s.occupiedBy.type == 2 and s.occupiedBy.side == moveNum % 2:
                                                        s.occupiedBy.enPassant = False
                                    
                                    if correct == False:
                                        break

                                    if choseMove == False:
                                        self.unhighlight_squares(B, moves)
                                        moves = []
                                        if B.board[sq].hasPiece:
                                            piece = B.board[sq].occupiedBy
                                            if (piece.side == moveNum % 2):
                                                moves = self.selectPiece(B, sq)
                                                self.highlight_squares(B, moves)
                                                selectedSquare = sq
                                                selected = True
                                            else:
                                                print("It is not your turn!")
                                        else:
                                            print("No piece here")
                                    else:
                                        choseMove = False
                            else:
                                # New game button
                                if (pos[0] < WIDTH // 3 and pos[0] >= 0) and (pos[1] < SCALE and pos[1] >= 0):
                                    self.playGame()

                                # Back to menu button
                                if (pos[0] < WIDTH and pos[0] >= 0) and (pos[1] < WIDTH + (SCALE*2) and pos[1] >= 1 * SCALE):
                                    return
                    
                    self.update_display(WIN, B, counter, winIn)
                    if correct == False:
                        break
                if correct == False:
                        break
            if correct:
                print("correct")
            else:
                break
        font = pygame.font.SysFont('timesnewroman.ttc', 100)
        text = font.render("Game Over!", True, RED)
        rect = text.get_rect()
        rect.center = (WIDTH / 2, WIDTH / 2)
        WIN.blit(text, rect)
        font = pygame.font.SysFont('timesnewroman.ttc', 48)

        test7 = " "
        if counter > int(score[0]):
            test7 = "New high score: " + str(counter)
            with open("chess_high_score.txt", "w") as out:
                out.write("{}\n".format(str(counter)))
            score_file.close()
        else:
            test7 = "Final score: " + str(counter)

        text2 = font.render(test7, True, RED)
        rect2 = text2.get_rect()
        rect2.center = (WIDTH / 2, WIDTH / 2 + 100)
        WIN.blit(text2, rect2)
        pygame.display.update()
        pygame.time.delay(3000)
        self.playGame()
