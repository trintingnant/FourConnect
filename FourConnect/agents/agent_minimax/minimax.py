import numpy as np

from agents.common import BoardPiece, apply_player_action, check_end_state, GameState

MAX_DEPTH = 10


def minValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int
        ) -> int:
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

        if depth == MAX_DEPTH or state != GameState.STILL_PLAYING:
            return state

        else:

            possible_moves = np.arange(7)
            minScore = -np.inf

            for move in possible_moves:

                new_board = apply_player_action(board, move, player)
                new_player = (player + 1) % 2
                score = maxValue(new_board, new_player, alpha, beta, depth-1)

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
) -> int:
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
    TODO: Implement IDDFS instead of DFS with cut-off
    """

    state = check_end_state(board, player)

    if depth == MAX_DEPTH or state != GameState.STILL_PLAYING:
        return state

    else:

        possible_moves =
        minScore = -np.inf

        for move in possible_moves:

            new_board = apply_player_action(board, move, player)
            new_player = (player + 1) % 2
            score = minValue(new_board, new_player, alpha, beta, depth-1)

            if score > maxScore:
                maxScore = score

            if maxScore > beta:
                return maxScore

            else:
                alpha = np.max(alpha, maxScore)

        return minScore


    def alphaBeta(
            board: np.array,
            player: BoardPiece,
            depth = MAX_DEPTH
    ) -> int:

        result = minValue(board, player, np.NINF, np.inf, depth=MAX_DEPTH)

        return result




    def generate_move_alphaBeta(np.board):

        """
        Generates the next move on the basis of traversal fo game-tree
        to MAX_DEPTH

        :return:
        TODO: Make this an iterative deepening search instead of DFS with cut-off
        """

        raise NotImplemented







