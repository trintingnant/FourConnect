import numpy as np
from collections import OrderedDict
from typing import Tuple, Optional

import agents.common as cm
from agents.heuristic import evaluateGame

# Hash function that hashes board positions to bitstrings
# to be used for transposition table in alphaBeta

def zobr_myhash_init(board: np.ndarray) -> np.ndarray:
    '''
    Initialises the hash table with hash values
    :param board: the game board
    :return: a hash table
    '''
    i,j = board.shape
    #Initialize the Hash table:
    htable = np.zeros((i,j,2))

    for row in range(i):
        for col in range(j):
            for player in range(2):
                htable[row, col, player] = np.random.randint(2**31-1, dtype=np.int64)

    return htable

board = cm.initialize_game_state()
zobr_myhash = zobr_myhash_init(board)

def hash_board(board: np.ndarray, htable: np.ndarray = zobr_myhash):

    i,j,k = htable.shape
    hashRes = 0

    for row in range(i):
        for col in range(j):

            if board[row,col] == cm.PLAYER1:
                hashRes ^= np.int64(htable[row,col,0])

            elif board[row,col] == cm.PLAYER2:
                hashRes ^= np.int64(htable[row,col,1])

    return hashRes




