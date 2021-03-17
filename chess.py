# Chess class
import pygame
import time
import sys

board = [[' ' for i in range(8)] for i in range(8)]




class Piece:
    def __init__(self, side, type, image, killable = False):
        self.side = side
        self.type = type
        self.killable = killable
        self.image = image

bPawn = Piece('b','p', 'chessImages/blackPawn.png')
bBishop = Piece('b', 'b', 'chessImages/blackBishop.png')
bKnight = Piece('b', 'n', 'chessImages/blackKnight.png')
bRook = Piece('b', 'r', 'chessImages/blackRook.png')
bQueen = Piece('b', 'q', 'chessImages/blackQueen.png')
bKing = Piece('b', 'k', 'chessImages/blackKing.png')

wPawn = Piece('w','p', 'chessImages/whitePawn.png')
wBishop = Piece('w', 'b', 'chessImages/whiteBishop.png')
wKnight = Piece('w', 'n', 'chessImages/whiteKnight.png')
wRook = Piece('w', 'r', 'chessImages/whiteRook.png')
wQueen = Piece('w', 'q', 'chessImages/whiteQueen.png')
wKing = Piece('w', 'k', 'chessImages/whiteKing.png')

def onBoard(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True

def toString(board):
    for i in board:
        for j in i:
            try:
                output += j.side + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output; 


class Chess:

    def printClass(self):
        print("This is the chess class.")