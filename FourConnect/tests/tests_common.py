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

    move = np.random.randint(7)

    board = apply_player_action(np.zeros((6,7)) move, player)

    assert isinstance(board, np.array)
    assert board.shape == (6,7)
    assert dtype == BoradPiece
    assert board[0, move] == player


def test_connected_four():

    from agents.common import connected_four

    board = np.zeros((6,7))
    board2 = board.copy()
    board[:,1] = np.ones(6) * player

    board2[0,:3] == np.ones(3) * player

    assert connected_four(board, player) == True
    assert connected_four(board2, player) == False









