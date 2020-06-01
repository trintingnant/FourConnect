import numpy as np
from collections import OrderedDict

from agents.common import BoardPiece, GameState, PLAYER1, PLAYER2, noPlayer
from agents.common import check_end_state, apply_player_action, initialize_game_state, pretty_print_board


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
        tempBoard = board.copy() #somehow this was necessary


        if depth == MAX_DEPTH or state != GameState.STILL_PLAYING:
            return state.value

        else:
            possible_moves = np.where(board[5] == noPlayer) #top row still empty
            minScore = np.inf

            for moveI, move in np.ndenumerate(possible_moves):

                new_board = apply_player_action(tempBoard, move, player)
                tempBoard = board.copy() #resetting tempBoard
                new_player = (player%2)+1
                score = maxValue(new_board, new_player, alpha, beta, depth+1)

                if score < minScore:
                    minScore = score

                if minScore <= alpha:
                    return minScore

                else:
                    beta = np.min((beta, minScore))

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
    tempBoard = board.copy()

    if depth == MAX_DEPTH:
        return state.value

    elif state != GameState.STILL_PLAYING:
        return state.value

    else:

        possible_moves = np.where(board[5] == noPlayer) #top row still empty
        maxScore = np.NINF

        for moveI, move in np.ndenumerate(possible_moves):

            new_board = apply_player_action(tempBoard, move, player)
            tempBoard = board.copy()
            new_player = (player%2)+1
            score = minValue(new_board, new_player, alpha, beta, depth+1)

            if score > maxScore:
                maxScore = score

            if maxScore >= beta:
                return maxScore

            else:
                alpha = np.max((alpha, maxScore))

        return maxScore


def alphaBeta(board: np.ndarray, player: BoardPiece, depth: int
) -> float:
    """
    Applies alphaBeta pruning to the minimax search from above
    :param board: the board
    :param player: the player
    :return: the score
    """
    #Call minValue for the current player: minValue because alphaBeta
    #will be called in the iterativeDeepning search for the minimizing player
    result = minValue(board, player, alpha=np.NINF, beta=np.inf, depth=depth)
    return result

def iterativeDeepingSearch(board: np.ndarray, player: BoardPiece
)-> np.ndarray:
    """
    Performs iterative deepening DFS on the search tree, which is advisable when
    moves are under time constraint. Does a full traversal of the game tree up to certain
    depth, then increments the depth. Only result from the last fuLl traversal of the tree
    should be considered.
    :param board: the board
    :param player: the player to move
    :param maxDepth: the maximal depth to which to search (temporary measure)
    :return: a list of moves with the best score
    """

    iter = MAX_DEPTH #sets cut-off depth for DFS: incrementally decreasing
    score = 0
    bestScore = np.NINF
    tempBoard = board.copy()
    tempBestScore = bestScore


    #Moves stored in OrderedDict: keys := score, vals := list(moves)
    #this will help (later on) with storing some of the suboptimal moves
    #and help circumvent some horizon problems
    bestMoves = OrderedDict()
    new_bestMoves = OrderedDict()

    #Generate list of best moves:
    #TODO: generate list of best and second (nth?) best moves
    #TODO: then draw move from a skewed (e.g. exponential) probability distribution
    #TODO: add time-limit related while-loop wrap

    #Generate a list of the best moves for iteration to next level:

    while iter > 0:

        possible_moves = np.where(board[5] == noPlayer)

        for moveI, move in np.ndenumerate(possible_moves):

            bestScore = tempBestScore

            new_board = apply_player_action(tempBoard, move, player)
            tempBoard = board.copy()
            new_player = (player%2)+1
            score = alphaBeta(new_board, new_player, iter)

            if score > bestScore:
                bestScore = score
                tempBestScore = bestScore
                new_bestMoves.clear()
                new_bestMoves[bestScore] = [move]


            #store all moves with the same score:
            elif score == bestScore:
                new_bestMoves[bestScore].append(move)
                #print(iter, new_bestMoves)

        #Check old and new bestScores are the same:
        if bestMoves != OrderedDict() and list(bestMoves.keys())[0] == list(new_bestMoves.keys())[0]:

            #Merge moves with the same score:
            new_bestMoves[list(bestMoves.keys())[0]] = bestMoves[list(bestMoves.keys())[0]] + \
                                                       new_bestMoves[list(new_bestMoves.keys())[0]]

        else:
            bestMoves = new_bestMoves.copy()

        new_bestMoves.clear()
        iter -= 1

        #Break if winning move has been found:
        if tempBestScore == GameState.IS_WIN.value:
            break

        tempBestScore = np.NINF

    #When under time constraint: check how deep you can go
    print("Iteration: {}".format(iter))
    keys, values = list(bestMoves.keys()), list(bestMoves.values())
    return keys, values



def generate_move_alphaBeta(board: np.array):

        """
        Generates the next move on the basis of traversal of game-tree
        to MAX_DEPTH

        :return:
        TODO: Make this an iterative deepening search instead of DFS with cut-off
        """

        raise NotImplemented








