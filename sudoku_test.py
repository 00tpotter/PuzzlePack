# Test suite for Sudoku game

import pytest
import numpy as np
import sudoku

@pytest.fixture
def getSudoku():  
    return sudoku.Sudoku()

# Arrange, get a blank board
@pytest.fixture
def getBoard(getSudoku):
    board = np.zeros([9, 9], dtype=np.int32)

    # Fill the array with -'s as placeholders
    for row in range(0, 9):
        for col in range(0, 9):
            board[row][col] = 0

    return board

# Arrange, get a filled board
@pytest.fixture
def getTestBoard(getSudoku):
    board = np.zeros([9, 9], dtype=np.int32)
    temp = [[9, 7, 8, 1, 3, 2, 4, 5, 6], 
             [4, 1, 5, 6, 8, 9, 3, 2, 7], 
             [2, 3, 6, 5, 7, 4, 1, 9, 8], 
             [7, 6, 2, 4, 5, 8, 9, 3, 1], 
             [1, 4, 3, 9, 6, 7, 2, 8, 5], 
             [8, 5, 9, 3, 2, 1, 7, 6, 4], 
             [5, 2, 7, 8, 1, 3, 6, 4, 9], 
             [6, 9, 1, 2, 4, 5, 8, 7, 3], 
             [3, 8, 4, 7, 9, 6, 5, 1, 2]]

    # Fill the array with -'s as placeholders
    for row in range(0, 9):
        for col in range(0, 9):
            board[row][col] = temp[row][col]

    return board

# Arrange, get a blank board
@pytest.fixture
def getTestOptBoard(getSudoku):
    board = np.zeros([9, 9], dtype=object)

    # Fill the array with -'s as placeholders
    for row in range(0, 9):
        for col in range(0, 9):
            board[row][col] = np.zeros([1], dtype=np.int32)

    return board


def test_printClass(getSudoku):
    result = getSudoku.printClass()
    test = "This is the Sudoku class."
    
    assert result == test

def test_checkRemove(getSudoku, getTestBoard, getTestOptBoard):
    result = getSudoku.checkRemove(getTestBoard, getTestOptBoard)

    assert result

def test_removeNum(getSudoku, getTestBoard, getTestOptBoard):
    result = getSudoku.removeNum(0, 0, getTestBoard, getTestOptBoard)
    test = getTestBoard
    test[0][0] = 0

    assert np.array_equal(result, test)

def test_fillBoard(getSudoku, getBoard):
    temp = getBoard
    getSudoku.fillBoard(0, 0, temp)
    test = getBoard

    for row in range(0, 9):
        for col in range(0, 9):
            assert temp[row][col] is not test[row][col]

def test_generateGame(getSudoku, getBoard):
    result = getSudoku.generateGame()
    test = getBoard

    for row in range(0, 9):
        for col in range(0, 9):
            assert result[row][col] is not test[row][col]
