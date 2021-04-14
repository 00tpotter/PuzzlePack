# Test suite for word search game

import pytest
import word_search

#class WordSearchTest:
    # def __init__(self):
    #     self.wordSearch = word_search.WordSearch()

def test_printClass():
    test = "This is the word search class."
    ws = word_search.WordSearch()
    assert ws.printClass() == test


    
