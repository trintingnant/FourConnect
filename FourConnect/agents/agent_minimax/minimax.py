import numpy as np

from agents.common import *

def minValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int
        ) -> GameState:
        """
        :param board: The game board
        :param state: The game state
        :param player: The player
        :param alpha: The parameter determining the cutoff for minValue
        :param beta: The parameter determining the cutoff for maxValue
        :param depth: The depth to which to perform traverse the tree
        this depth will be iteratively after the tree has been traversed
        completely at all shallower depths (iterative deepening search)
        :return: A Gamestate corresponding to the best outcome for the
        opponent player under optimal play
        """

        state = check_end_state(board, player)

        if depth == 0 or state != GameState.STILL_PLAYING:
            return state

        else:

            possible_moves = np.arange(7)
            minScore = -np.inf

            for move in possible_moves:

                new_board = apply_player_action(board, move, player)
                score = maxValue(new_board, player, alpha, beta, depth-1)

                if score < minScore:
                    minScore = score

                if minScore <= alpha:
                    return minScore

                else:
                    beta = np.min(beta, minScore)

            return minScore


def maxValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int
) -> GameState:
    """
    :param board: The game board
    :param state: The game state
    :param player: The player
    :param alpha: The parameter determining the cutoff for minValue
    :param beta: The parameter determining the cutoff for maxValue
    :param depth: The depth to which to perform traverse the tree
    this depth will be iteratively after the tree has been traversed
    completely at all shallower depths (iterative deepening search)
    :return: A Gamestate corresponding to the best outcome for the
    opponent player under optimal play
    """

    state = check_end_state(board, player)

    if depth == 0 or state != GameState.STILL_PLAYING:
        return state

    else:

        possible_moves = np.arange(7)
        minScore = -np.inf

        for move in possible_moves:

            new_board = apply_player_action(board, move, player)
            score = minValue(new_board, alpha, beta, )

            if score > m:
                minScore = score

            if minScore <= alpha:
                return minScore

            else:
                beta = np.min(beta, minScore)

        return minScore







