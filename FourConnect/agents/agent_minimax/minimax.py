import numpy as np
from collections import OrderedDict

from agents.common import BoardPiece, GameState, PLAYER1, PLAYER2, noPlayer
from agents.common import check_end_state, apply_player_action, initialize_game_state


MAX_DEPTH: int = 10
TIME_THRESHOLD: int = 2000
timeOut: bool


def minValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int
) -> float:
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
            possible_moves = np.where(board[5] == noPlayer)#top row still empty
            minScore = np.inf

            for move in possible_moves:

                new_board = apply_player_action(board, move, player)
                new_player = (player + 1) % 2
                score = maxValue(new_board, new_player, alpha, beta, depth+1)

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
) -> float:
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

        possible_moves = np.where(board[5] == noPlayer) #top row still empty
        maxScore = np.NINF

        for move in possible_moves:

            new_board = apply_player_action(board, move, player)
            new_player = (player + 1) % 2
            score = minValue(new_board, new_player, alpha, beta, depth+1)

            if score > maxScore:
                maxScore = score

            if maxScore > beta:
                return maxScore

            else:
                alpha = np.max(alpha, maxScore)

        return maxScore


def alphaBeta(board: np.ndarray, player: BoardPiece, depth: int
) -> float:
    """
    Applies alphaBeta pruning to the minimax search from above
    :param board: the board
    :param player: the player
    :return: the score
    """
    #Call minValue for the current player:
    result = minValue(board, player, np.NINF, np.inf, depth=depth)
    return result

def iterativeDeepingSearch(board: np.ndarray, player: BoardPiece
)-> np.ndarray:
    """
    :param board: the board
    :param player: the player to move
    :param maxDepth: the maximal depth to which to search (temporary measure)
    :return: a list of moves with the best score
    """

    iter = MAX_DEPTH #sets cut-off depth for DFS: incrementally decreasing
    score, bestScore = 0, np.NINF

    possible_moves = np.where(board[5] == noPlayer)
    #Moves stored in OrderedDict: keys := score, vals := list(moves)
    #this will help (later on) with storing some of the suboptimal moves
    #and help circumvent some horizon problems
    bestMoves = OrderedDict()
    new_bestMoves = OrderedDict()

    #Generate list of best moves:
    #TODO: generate list of best and second (nth?) best moves
    #TODO: then draw move from a skewed probability distribution
    #TODO: add time-limit related while-loop wrap

    #Generate a list of the best moves for iteration to next level:

    while iter >= 0:

        for move in possible_moves:

            new_state = apply_player_action(board, move, player)
            new_player = (player + 1) % 2
            score = alphaBeta(new_state, new_player, iter)

            if score > bestScore:
                bestScore = score
                new_bestMoves.clear()
                new_bestMoves[bestScore] = [move]

            #store all moves with the same score:
            elif score == bestScore:
                new_bestMoves[bestScore].append(move)

        #Check old and new bestScores are the same:
        if bestMoves != OrderedDict() and list(bestMoves.keys())[0] == list(new_bestMoves.keys())[0]:

            #Merge moves with the same score:
            bestMoves[list(bestMoves.keys())[0]] + new_bestMoves[list(new_bestMoves.keys())[0]]

        else:
            bestMoves = new_bestMoves

        new_bestMoves.clear()
        iter -= 1
        bestScore = np.NINF

    #When under time constraint: check how deep you can go
    print("Iteration: {}".format(iter))
    return bestMoves

print(iterativeDeepingSearch(initialize_game_state(), PLAYER1))


















def generate_move_alphaBeta(board: np.array):

        """
        Generates the next move on the basis of traversal of game-tree
        to MAX_DEPTH

        :return:
        TODO: Make this an iterative deepening search instead of DFS with cut-off
        """

        raise NotImplemented

print(minValue)





