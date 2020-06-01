
#Implements and tests different versions of the connect_four method:
#:param board: the board to be checked
#:param player: the player for whom to check
#:param last_action: the last action performed
#:return bool: does player have connectN pieces in a row?


disable_jit = False
if disable_jit:
    import os
    os.environ['NUMBA_DISABLE_JIT'] = '1'

import timeit
import numpy as np
from numba import njit
from typing import Optional, Tuple
from agents.common import initialize_game_state, BoardPiece
from agents.common import PlayerAction, connectN, players, PLAYER1, PLAYER2, noPlayer

@njit()
def connected_four_iter(
    board: np.ndarray, player: BoardPiece, _last_action: Optional[PlayerAction] = None
) -> bool:
    rows, cols = board.shape
    rows_edge = rows - connectN + 1
    cols_edge = cols - connectN + 1

    for i in range(rows):
        for j in range(cols_edge):
            if np.all(board[i, j:j+connectN] == player):
                return True

    for i in range(rows_edge):
        for j in range(cols):
            if np.all(board[i:i+connectN, j] == player):
                return True

    for i in range(rows_edge):
        for j in range(cols_edge):
            block = board[i:i+connectN, j:j+connectN]
            if np.all(np.diag(block) == player):
                return True
            if np.all(np.diag(block[::-1, :]) == player):
                return True

    return False

def connected_four_flips(board: np.ndarray, player: BoardPiece, _last_action: Optional[PlayerAction] = None
) -> bool:

    """
    Function that finds connectN pieces by moving through rows, cols and diags of the board, incrementing
    a counter (very bad, here only for reasons of performance comparison)
    :param board: --"--
    :param player: --"--
    :param _last_action: --"--
    :return:
    """

    def boardChecker(board: np.ndarray, player: BoardPiece, number=connectN
                     ) -> bool:
        result = False
        for i in range(len(board)):
            counter = 0
            for j in range(len(board[i])):
                if counter == number:
                    result = True
                    break
                else:
                    counter += 1 if board[i][j] == player else -counter
        return result

    # Extract all possible diagonals from the board:
    diags = lambda array: np.array([np.diag(arr) for arr in [array[:, i:6] for i in np.arange(0, 6, 1)]]\
                                   + [np.diag(arr) for arr in [array.T[:, 0:i] for i in np.arange(6, 0, -1)]]\
                                   + [np.diag(arr) for arr in [np.flipud(array)[:, i:6] for i in np.arange(0, 6, 1)]]\
                                   + [np.diag(arr) for arr in
                                      [np.flipud(array).T[:, 0:i] for i in np.arange(6, 0, -1)]])

    boards = [board, board.T, diags(board)]
    # Apply boardChecker function to rows, columns and diagonals:
    func = lambda brd: boardChecker(brd, player)

    return func(board) or func(board.T) or func(diags(board))



def estimate_running_times(numIters: int=10, numBoardIters: int=int(10e4)) -> Tuple[float]:

    '''
    Estimates the running times of the different methods for finding connected pieces
    :param numIters: The number of different boards on which to test the function
    :param numBoardIters: The number of times the function is run on the same board
    :return:
    '''

    counter = 0
    res1, res2 = np.zeros((2, numIters))

    while counter < numIters:
        
        print(counter) #track progress

        board = np.random.choice(players, ((6, 7)))
        player = np.random.choice(players[:2])

        res1[counter] = timeit.timeit("connected_four_iter(board, player)",
                    setup="connected_four_iter(board, player)",
                    number=numBoardIters,
                    globals=dict(connected_four_iter=connected_four_iter,
                                 board=board,
                                 player=player))
        res1[counter] / numBoardIters * 1e6

        res2[counter] = timeit.timeit("connected_four_flips(board, player)",
                    setup="connected_four_flips(board, player)",
                    number=numBoardIters,
                    globals=dict(connected_four_flips=connected_four_flips,
                                 board=board,
                                 player=player))
        res2[counter] / numBoardIters * 1e6

        counter += 1

    return res1.mean(), res2.mean()


#Iterative procedure far superior to flipping procedure:
runTimeEst = estimate_running_times()

print(f"Python iteration-based: {runTimeEst[0]: .1f} us per call")
print(f"Python flip-based: {runTimeEst[1]: .1f} us per call")






