import numpy as np
import re

import warnings

from enum import Enum
from typing import Optional, Callable, Tuple
from errors.errors import ColumnError, BoardError
import timeit

BoardPiece = np.int8

noPlayer = BoardPiece(0)
PLAYER1 = BoardPiece(1)
PLAYER2 = BoardPiece(2)
players = np.array([PLAYER1, PLAYER2, noPlayer])

PlayerAction = np.int8
connectN: np.int8 = 4

class SavedState:
    pass

GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]

class GameState(Enum):
    IS_WIN = 1000
    IS_DRAW = -10
    IS_LOSS = -1000
    STILL_PLAYING = 0

class SavedState:
    pass

#TODO: Convert every to bitmap representation!!

def initialize_game_state() -> np.ndarray:
    """
    Intializes the board
    :return: np.ndarray with dimension : 6 x 7
    """
    return np.zeros((6, 7), dtype=BoardPiece)

def pretty_print_board(board: np.ndarray):

    """
    Pretty-prints the Four Connect board
    :param board: the board to be printed
    :return: a string representation of the board
    """

    flipBoard = np.flipud(board) #correct orientation

    # Separator for printed rows:
    sepa = ('\t' + '|' + '\n')

    # The bottom and the top of the playing board
    bottomtop = '|' + '='*31 + '|' + '\n'

    # The last row:
    lrow = sepa.join(['\t'.join(['|'] + [str(i) for i in range(7)])]) + sepa

    #Make a dictionary that converts keys into their board represenations:
    board_rep = {str(PLAYER1): 'X', str(PLAYER2): 'O', str(noPlayer): ' '}

    #Draw the board:
    ppBoard = (sepa.join(['\t'.join (['|'] + [board_rep[str(int(cell))] for cell in row]) for row in flipBoard]))
    ppBoard = bottomtop + ppBoard + sepa + bottomtop + lrow

    print(ppBoard)

    return ppBoard


def string_to_board(np_board: str) -> np.ndarray:
    """
    Takes a string representation of a board as input and return the respective array
    :param np_board: the string representation of the board
    :return: the board
    """

    # Weed out all spurious symbols with pattern matching:
    board = re.sub("[0-9]|=|\t|\n|\|",'', np_board)

    # Make a dictionary that converts keys into their board representations
    board_rep = {PLAYER1: 'X', PLAYER2: 'O', noPlayer: ' '}

    #Get keys & values:
    board_vals, board_keys = list(board_rep.keys()), list(board_rep.values())

    #Decode string:
    result = np.array(list(map(lambda key: board_vals[board_keys.index(key)], board))).reshape(6, 7)

    return np.flipud(result)


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


    #Raise exception if action is not a column:

    if not action in range(board.shape[1]):
        raise BoardError("Not a board column")
        return board

    #Raise exception if row is full:

    if board[-1, action] != noPlayer:
        raise ColumnError("Column already full")
        return board

    bottom = np.min(np.where(board[:, action] == noPlayer))
    board[bottom, action] = player

    return board


def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:

    import agents.connect_four as connect_four

    """
    Returns whether the game is a win for the current player
    :param board: the board before last_action
    :param player: the player
    :param last_action: the last_action
    :return:
    """

    return connect_four.connected_four_iter(board, player, last_action)

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

    elif connected_four(board,(player%2)+1):
        return GameState.IS_LOSS

    elif np.size(board[board == 0]) != 0:
        return GameState.STILL_PLAYING

    else: #no free cells remaining
        return GameState.IS_DRAW




