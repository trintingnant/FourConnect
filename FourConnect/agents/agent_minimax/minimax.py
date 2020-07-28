import numpy as np
from collections import OrderedDict
from typing import Tuple, Optional


from agents.common import BoardPiece, GameState, PLAYER1, PLAYER2, noPlayer, SavedState, PlayerAction
from agents.common import check_end_state, apply_player_action, initialize_game_state, pretty_print_board
from agents.heuristic import evaluateGame
from agents.hashing import zobr_myhash_init, hash_board


MAX_DEPTH: int = 6
TIME_THRESHOLD: int = 2000
timeOut: bool

global htable, transpoTable, transpo_size
htable = zobr_myhash_init(initialize_game_state())
transpoTable = OrderedDict()
transpo_size = 50



def minValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int,
        lastMove: Optional[PlayerAction],
        movesPlayed: OrderedDict()
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


        if state != GameState.STILL_PLAYING:
            return -state.value

        elif depth == MAX_DEPTH:
            return -evaluateGame(board, player, lastMove)

        else:
            #Determine the order in which moves are explored
            #Moves that are played often are explored first
            sorted(movesPlayed.items(), key=lambda item: item[1])
            possible_moves = np.array(list(movesPlayed.keys()))
            possible_moves = possible_moves[board[5] == noPlayer] #top row still empty
            minScore = np.inf

            for moveI, move in np.ndenumerate(possible_moves):

                movesPlayed[lastMove] += 1

                new_board = apply_player_action(tempBoard, move, player)
                tempBoard = board.copy() #resetting tempBoard
                new_player = player % 2 + 1
                score = maxValue(new_board, new_player, alpha, beta, depth+1, \
                                 lastMove=move, movesPlayed=movesPlayed)

                if score < minScore:
                    minScore = score

                if minScore <= alpha:
                    return minScore

                #TODO: Random pruning: with small probability, prune anyway

                else:
                    beta = np.min((beta, minScore))

        return minScore


def maxValue(
        board: np.ndarray,
        player: BoardPiece,
        alpha: float,
        beta: float,
        depth: int,
        lastMove: Optional[PlayerAction],
        movesPlayed: OrderedDict
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

    if state != GameState.STILL_PLAYING:
        return state.value

    elif depth == MAX_DEPTH:
        return evaluateGame(board, player, lastMove)

    else:
        sorted(movesPlayed.items(), key=lambda item: item[1])
        possible_moves = np.array(list(movesPlayed.keys()))
        possible_moves = possible_moves[board[5] == noPlayer]  # top row still empty
        maxScore = np.NINF

        for moveI, move in np.ndenumerate(possible_moves):

            movesPlayed[lastMove] += 1
            lastMove = move

            new_board = apply_player_action(tempBoard, move, player)
            tempBoard = board.copy()
            new_player = player % 2 + 1
            score = minValue(new_board, new_player, alpha, beta, depth+1, \
                             lastMove=move, movesPlayed=movesPlayed)

            if score > maxScore:
                maxScore = score

            if maxScore >= beta:
                return maxScore
            #TODO: Random pruning: with small probability, prune anyway

            else:
                alpha = np.max((alpha, maxScore))

        return maxScore


def alphaBeta(board: np.ndarray, player: BoardPiece, depth: int, lastMove: Optional[PlayerAction]
) -> float:
    """
    Applies alphaBeta pruning to the minimax search from above
    :param board: the board
    :param player: the player
    :return: the score
    """
    #Passes OrderedDict with moves that have been played for ordering search tree
    movesPlayed = OrderedDict([(i,0) for i in np.arange(7)])
    #Call minValue for the current player: minValue because alphaBeta
    #will be called in the iterativeDeepning search for the minimizing player
    result = minValue(board, player, alpha=np.NINF, beta=np.inf, depth=depth,\
                      lastMove=lastMove, movesPlayed=movesPlayed)
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

    #Early in the game: play moves in the center columns:

    while iter > 0:

        possible_moves = np.where(board[5] == noPlayer)

        for moveI, move in np.ndenumerate(possible_moves):

            last_move = move
            score = np.NINF

            bestScore = tempBestScore

            new_board = apply_player_action(tempBoard, move, player)
            #Check if new_board is in the transposition table:
            hash_key = hash_board(new_board)

            if transpoTable.get(hash_key) is not None:
                score = transpoTable[hash_key]

            else:
                tempBoard = board.copy()
                new_player = (player%2)+1
                score = alphaBeta(new_board, new_player, iter, last_move)

            if score > bestScore:
                bestScore = score
                tempBestScore = bestScore
                new_bestMoves.clear()
                new_bestMoves[bestScore] = [move]
                transpoTable[hash_key] = bestScore

                # FIFO queue, pop item upon exceeding space limit
                if len(list(transpoTable.keys())) > transpo_size:
                    transpoTable.popitem()


            #store all moves with the same score:
            elif score == bestScore:
                new_bestMoves[bestScore].append(move)
                transpoTable[hash_key] = bestScore
                if len(list(transpoTable.keys())) > transpo_size:
                    transpoTable.popitem()

        #Check old and new bestScores are the same:
        if bestMoves != OrderedDict() and list(bestMoves.keys())[0] == list(new_bestMoves.keys())[0]:

            #Merge moves with the same score: my guess is this will be important when the heuristic
            #is such that it creates the same value a lot of the time and no computational concern otherwise
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

def generate_move_alphaBeta(board: np.array, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
        """
        Generates next move
        :param board: the initial board
        :param player: the player
        :return: an action
        """
        # Early in the game: play moves in the center columns:
        if np.count_nonzero(board) < 2:
            move = 3
            return move, saved_state

        scores, actions = iterativeDeepingSearch(board, player)
        #Randomly select one of the moves:
        move = np.random.choice(actions[0]) #that's pretty ugly
        return move, saved_state


