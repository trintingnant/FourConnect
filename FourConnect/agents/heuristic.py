import numpy as np
from typing import Optional
from agents.common import GameState, BoardPiece, PLAYER1, PLAYER2, PlayerAction, check_end_state, noPlayer
from agents.common import initialize_game_state

#TODO: add a small hashtable that stores positions that have already been explored

def  evaluateGame(board: np.ndarray, player: BoardPiece, lastMove: Optional[PlayerAction]) -> float:
    '''
    Evaluates boards that are not of any of the Game.State.STILL_PLAYING type
    :param board: the board to be evaluated
    :return: a value that ideally representing the quality of the board
    '''

    # Kernel that assigns weights to pieces in the respective rows/columns
    colKernel = np.array([1, 2, 6, 12, 6, 2, 1])
    rowKernel = np.array([1,2,4,4,2,1])
    opponent = player % 2 + 1

    #Heuristic that biases agent toward playing up the middle columns:
    def kernel_heuristic(board: np.ndarray, player: BoardPiece) -> float:
        colValue = (np.where(board==player, 1, 0)*colKernel).sum() - (np.where(board==opponent, 1, 0)*colKernel).sum()
        #rowValue = (np.where(board.T==player, 1, 0)*rowKernel).sum() - (np.where(board.T==opponent, 1, 0)*rowKernel).sum()

        return colValue

    #Heuristic that biases playing into columns with lots of free positions:
    def sky_heuristic(board: np.ndarray, player: BoardPiece, lastMove: Optional[PlayerAction]) -> float:
        if lastMove==None:
            return 0
        else:
            clouds = np.where(board==noPlayer, 1, 0)
            clouds = clouds.sum(axis=0)
        return 70*clouds[lastMove] / clouds.sum()


    #Heuristic that biases topping columns:
    def top_heuristic(board: np.ndarray, player: BoardPiece) -> float:

        mask = (board != noPlayer).argmax(axis=0) #get topmost non-zero elements
        score = 0

        for (i,j) in zip(np.arange(7), mask):
            score += colKernel[i] if mask[j]==player else -colKernel[i]
        return score

    #Heuristic that penalizes topping columns too early:
    def tooQuickheuristic(board: np.ndarray, player: BoardPiece) -> float:
        if not np.count_nonzero(board)<=41:
            return np.count_nonzero(board) * board[board==player].argmax(axis=0)
        else:
            return 0

    #These aren't working spectacularly to be honest

    return kernel_heuristic(board, player)



