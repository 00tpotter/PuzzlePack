# Chess class
import pygame
import time
import sys
from typing import List

WIDTH = 800
squareSize = WIDTH / 8
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)



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
        pygame.draw.rect(WIN, self.color, (self.x, self.y, squareSize, squareSize))
        if self.hasPiece:
            WIN.blit(self.occupiedBy.image, (self.x, self.y))
        if self.highlighted:
            pygame.draw.circle(WIN, GREY, (self.x + squareSize/2, self.y + squareSize/2), 15)

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
        for i in range(len(fen)):
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

def selectPiece(B, index):
    piece = B.board[index].occupiedBy
    if piece.type == 2:
        if piece.side == 0:
            return pawn_moves_w(B, index)
        else:
            return pawn_moves_b(B, index)
    elif piece.type == 1:
        return king_moves(B, index)
    elif piece.type == 3:
        return knight_moves(B, index)
    elif piece.type == 4:
        return bishop_moves(B, index)
    elif piece.type == 5:
        return rook_moves(B, index)
    elif piece.type == 6:
        return queen_moves(B, index)

def pawn_moves_w(B, index):
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
    return moves

def pawn_moves_b(B, index):
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
    return moves

def knight_moves(B, index):
    moves = []
    
    side = B.board[index].occupiedBy.side
    i = int(index / 8)
    j = index % 8

    for x in range(-2, 3):
        for y in range(-2, 3):
            if x ** 2 + y ** 2 == 5:
                if on_board((x + i, y + j)):
                    if B.board[index + 8*x + y].hasPiece == False:
                        moves.append(index + x*8 + y)
                    elif B.board[index + 8*x + y].occupiedBy.side != side:
                        moves.append(index + x*8 + y)
    return moves

def bishop_moves(B, index):
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
            if on_board(position):
                posIndex = position[0] * 8 + position[1]
                if B.board[posIndex].hasPiece == False:
                    moves.append(posIndex)
                elif B.board[posIndex].occupiedBy.side != side:
                    moves.append(posIndex)
                    break
                else:
                    break

    return moves

def rook_moves(B, index):
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
            if on_board(position):
                posIndex = position[0] * 8 + position[1]
                if B.board[posIndex].hasPiece == False:
                    moves.append(posIndex)
                elif B.board[posIndex].occupiedBy.side != side:
                    moves.append(posIndex)
                    break
                else:
                    break

    return moves

def queen_moves(B, index):
    m1 = bishop_moves(B, index)
    m2 = rook_moves(B, index)
    for i in m2:
        m1.append(i)
    return m1

def king_moves(B, index):
    moves = []
    side = B.board[index].occupiedBy.side
    i = int(index / 8)
    j = index % 8
    pairs = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], 
             [i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
    for position in pairs:
        if on_board(position):
            posIndex = position[0] * 8 + position[1]
            if B.board[posIndex].hasPiece == False:
                moves.append(posIndex)
            elif B.board[posIndex].occupiedBy.side != side:
                moves.append(posIndex)
    return moves

def on_board(position):
    if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
        return False
    return True

def highlight_squares(B, moves):
    for i in moves:
        B.board[i].highlight()

def unhighlight_squares(B, moves):
    for i in moves:
        B.board[i].unhighlight()

def update_display(win, Board):
    for square in Board.board:
        square.draw(win)
        pygame.display.update()

def findNode(pos):
    x,y = pos
    row = y // squareSize
    col = x // squareSize
    return int(row)*8 + int(col)

def main(WIN, WIDTH):
    B = Board()
    B.positionFromFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    B.printBoard()
    pygame.init()
    moveNum = 0
    moves = []
    selected = False
    selectedSquare = -1
    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                sq = findNode(pos)
                if selected == False:
                    if B.board[sq].hasPiece:
                        piece = B.board[sq].occupiedBy
                        if (piece.side == moveNum % 2):
                            moves = selectPiece(B, sq)
                            highlight_squares(B, moves)
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
                            B.board[sq].placePiece(piece)
                            B.board[selectedSquare].movePiece()
                            selectedSquare = -1
                            selected = False
                            unhighlight_squares(B, moves)
                            moves = []
                            moveNum += 1
                            choseMove = True
                    if choseMove == False:
                        unhighlight_squares(B, moves)
                        moves = []
                        if B.board[sq].hasPiece:
                            piece = B.board[sq].occupiedBy
                            if (piece.side == moveNum % 2):
                                moves = selectPiece(B, sq)
                                highlight_squares(B, moves)
                                selectedSquare = sq
                                selected = True
                            else:
                                print("It is not your turn!")
                        else:
                            print("No piece here")
                    else:
                        choseMove = False





            update_display(WIN, B)

    
class Chess:
    main(WIN, WIDTH)

