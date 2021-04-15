# Test suite for word search game

import pytest
import numpy as np
import word_search

@pytest.fixture
def getWS():  
    return word_search.WordSearch()

# Arrange, get a blank board
@pytest.fixture
def getBoard(getWS):
    board = np.zeros([getWS.size, getWS.size], dtype=str)

    # Fill the array with -'s as placeholders
    for row in range(0, getWS.size):
        for col in range(0, getWS.size):
            board[row][col] = "-"

    return board

def test_printClass(getWS):
    result = getWS.printClass()
    test = "This is the word search class."
    
    assert result == test

def test_checkWord(getWS, getBoard):
    result = getWS.checkWord("test", 0, 0, "E", getBoard)

    assert result

def test_fillWord(getWS, getBoard):
    x = 0
    y = 0
    word = "test"
    result = getWS.fillWord(word, x, y, "E", getBoard)
    test = getBoard
    for i in range(0, len(word)):
        test[x+i][y] = word[i:i+1]

    assert np.array_equal(result, test)

def test_addWord(getWS, getBoard):
    x = 0
    y = 0
    word = "test"
    result = getWS.addWord("test", 0, 0, "E", getBoard)
    test = getBoard
    for i in range(0, len(word)):
        test[x+i][y] = word[i:i+1]
    

    assert np.array_equal(result, test)

def test_generateGame(getWS, getBoard):
    result = getWS.generateGame()
    test = getBoard

    for row in range(0, getWS.size):
        for col in range(0, getWS.size):
            assert result[row][col] is not test[row][col]
