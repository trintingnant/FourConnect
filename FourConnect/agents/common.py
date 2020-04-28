import numpy as np

import warnings

from enum import Enum
from typing import Optional

BoardPiece = np.int8

noPlayer = BoardPiece(0)
Player1 = BoardPiece(1)
Player2 = BoardPiece(2)

PlayerAction = np.int8

class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0

def initialize_game_state() -> np.ndarray:
    """
    Intializes the board
    :return: np.ndarray with dimension : 6 x 7
    """

    return np.zeros((6,7), dtype=BoardPiece)

def pretty_print_board(board: np.ndarray):

    """
    Pretty-prints the Four Connect board
    :param board: the board to be printed
    :return: a string representation of the board
    """
    # Separator for printed rows:
    sepa = ('\t' + '|' + '\n')

    # The bottom and the top of the playing board
    bottomtop = '|' + '='*31 + '|' + '\n'

    # The last row:
    lrow = sepa.join(['\t'.join(['|'] + [str(i) for i in range(7)])]) + sepa

    #Make a dictionary that converts keys into their board represenations:

    board_rep = {str(Player1): 'X', str(Player2): 'O', str(noPlayer): ' '}

    #Draw the board:

    ppBoard = (sepa.join(['\t'.join (['|'] + [board_rep[str(int(cell))] for cell in row]) for row in board]))

    ppBoard = bottomtop + ppBoard + sepa + bottomtop + lrow

    return ppBoard

    pp



"""
def string_to_board(np_board: str) -> np.ndarray:

    # Make a dictionary that converts keys into their board representations
    # (I think, just in this case, using this twice is better than making it global).

    board_rep = {str(Player1): 'X', str(Player2): 'O', str(noPlayer): ' '}

    board_vals, board_keys = list(board_rep.keys()), np.array(list(board_rep.values()))

    return np.array(list(filter(lambda key: board_keys[board_vals.index(key)], np_board))).reshape(6,7)

"""

def apply_player_action(
        board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False
) -> np.ndarray:
    """
    Sets board[i,action] = player, where i is the lowest open row.
    the modified board is returned
    :param board: The initial board
    :param action: The action (i.e. the column the player chooses)
    :param player: The player who's turn it is
    :param copy:
    :return: a new board
    """

    #Raise exception if row is full:

    if board[-1, action] != noPlayer:

        raise Exception ("column already full")

        return board

    bottom = np.min(np.where(board[:, action] == noPlayer))

    board[bottom, action] = player

    return board



def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:

    #TODO: Improve the way the connected pieces are found -> bitmap?
    """
    Returns whether the game is a win for the current player
    :param board: the board before last_action
    :param player: the player
    :param last_action: the last_action
    :return:
    """

    #Extract all possible diagonals from the board:

    diags = lambda array: np.array([np.diag(arr) for arr in [array[:,i:6] for i in np.arange(0, 6, 1)]]\
                                   + [np.diag(arr) for arr in [array.T[:,0:i] for i in np.arange(6, 0, -1)]]\
                                   + [np.diag(arr) for arr in [np.flipud(array)[:, i:6] for i in np.arange(0, 6, 1)]]\
                                   + [np.diag(arr) for arr in [np.flipud(array).T[:, 0:i] for i in np.arange(6, 0, -1)]])

    boards = [board, board.T, diags(board)]

    #Apply boardChecker function to rows, columns and diagonals:

    func = lambda brd: boardChecker(brd, player, 4)

    return func(board) or func(board.T) or func(diags(board))


def boardChecker(
        board : np.ndarray, player: BoardPiece, number: int
) -> bool:

    """
    Helper function for connected_four: checks a row for n-time consective
    occurence of the same item (i.e. player)

    :param row: the board
    :param player: the player
    :param number: the number of consecutive occurences to be checked
    :return: Does the board have "number" consecutive stones by one player
    """

    result = False

    for i in range(len(board)):

        counter = 0

        for j in range(len(board[i])):

            if counter == number:

                result = True

                break

            else:

                counter += 1 if board[i][j] == player else -counter

    return False

def check_end_state(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    :param board:
    :param player:
    :param last_action:
    :return: The game state
    """

    if connected_four(board, player):

        return GameState.IS_WIN

    elif np.size(board[board == 0]) != 0:

        return GameState.STILL_PLAYING

    else:

        return GameState.IS_DRAW

res = pretty_print_board(initialize_game_state())













