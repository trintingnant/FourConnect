import numpy as np

from agents.common import BoardPiece, noPlayer

#Tests for Initialization:

def test_initialize_game_state():

    from agents.common import initialize_game_state

    board = initialize_game_state()

    assert isinstance(board, np.array)
    assert board.shape == (6,7)
    assert board.dtype == BoardPiece
    assert np.array_equal(board, np.zeros((6,7)))


#Test for Player action:

def test_apply_player_action():

    from agents.common import apply_player_action

    assert isinstance(board, np.array)
    assert board.shape == (6,7)
    assert dtype == BoradPiece
    assert np.a



