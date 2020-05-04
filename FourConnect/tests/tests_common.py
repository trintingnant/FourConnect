import numpy as np

from agents.common import BoardPiece, PlayerAction, GameState, PLAYER1, PLAYER2

player = PLAYER1

#Tests for Initialization:

def test_initialize_game_state():

    from agents.common import initialize_game_state

    board = initialize_game_state()

    assert isinstance(board, np.ndarray)
    assert board.shape == (6,7)
    assert board.dtype == BoardPiece
    assert np.array_equal(board, np.zeros((6,7)))


#Test for Player action:

def test_apply_player_action():

    from agents.common import apply_player_action

    move = np.random.randint(7)

    board = apply_player_action(np.zeros((6,7)), move, player)

    assert isinstance(board, np.ndarray)
    assert board.shape == (6,7)
    assert board[0, move] == player if move in np.arange(7) \
        else np.all(board == np.zeros((6,7)))



def test_connected_four():

    from agents.common import connected_four

    board = np.zeros((6,7))
    board2 = board.copy()
    board[:,1] = np.ones(6) * player

    assert connected_four(board, player) == True
    assert connected_four(board2, player) == False

def test_check_end_state():

    from agents.common import check_end_state

    board = np.zeros((6,7))
    board[:,3] = np.ones(6)

    assert check_end_state(board, player) == GameState.IS_WIN
    assert check_end_state(board.T, player) == GameState.IS_WIN
    assert check_end_state(board, PLAYER2) != GameState.IS_WIN

print(test_initialize_game_state(),
      test_connected_four(),
      test_check_end_state(),
      test_apply_player_action())










