# Test suite for minesweeper game

import pytest
import minesweeper


@pytest.fixture
def getMinesweeper():
    return minesweeper.Minesweeper()

def test_reveal(getMinesweeper):
    x = 1
    y = 1
    result = getMinesweeper.board.board[x][y].reveal()
    expected = True

    assert result == expected


def test_find_node(getMinesweeper):
    x = 0
    y = 0
    rows = getMinesweeper.rows

    result = getMinesweeper.findNode([x, y], rows)
    expected = [0,0]

    assert result == expected

