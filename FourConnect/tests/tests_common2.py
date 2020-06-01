import numpy as np
import unittest

from agents.common import BoardPiece, PlayerAction, GameState, PLAYER1, PLAYER2, noPlayer

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

    #Intialize board with full column, check is function returns the same board

    board[:,move] = np.ones(6)*player




def test_connected_four():

    from agents.common import connected_four

    board = np.zeros((6,7))
    board2 = board.copy()
    board[:,1] = np.ones(6) * player

    assert connected_four(board, player) == True
    assert connected_four(board2, player) == False

def test_check_end_state():

    from agents.common import check_end_state

    board= np.zeros((6,7))
    board2 = board.copy()
    board[:,3] = np.ones(6)
    board2[:4, 3] = np.zeros(4)

    assert check_end_state(board, player) == GameState.IS_WIN
    assert check_end_state(board.T, player) == GameState.IS_WIN
    assert check_end_state(board, PLAYER2) != GameState.IS_WIN
    assert check_end_state(board2, player) == GameState.STILL_PLAYING
    assert check_end_state(board, PLAYER2) == GameState.STILL_PLAYING

def test_string_to_board():

    from agents.common import string_to_board, pretty_print_board

    board = np.random.choice([PLAYER2, PLAYER2, noPlayer], (6,7))

    assert np.array_equal(string_to_board(pretty_print_board(board)), board)



def test_pretty_print_board():

    from agents.common import pretty_print_board






print(test_initialize_game_state(),
      test_connected_four(),
      test_check_end_state(),
      test_apply_player_action(),
      test_string_to_board())










