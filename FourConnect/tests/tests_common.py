import numpy as np
import unittest
import sys, os

#Block annoying prints from the pprint function:
def blockPrinting():
    sys.stdout = open(os.devnull, 'w')

def unblockPrinting():
    sys.stdout = sys.__stdout__

blockPrinting()

from agents.common import BoardPiece, PlayerAction, GameState, PLAYER1 as player, PLAYER2, noPlayer
from agents.common import initialize_game_state
from errors.errors import ColumnError, BoardError

class testCommon(unittest.TestCase):

    def testApplyPlayerAction(self):

        from agents.common import apply_player_action

        move = np.random.randint(7)
        board = apply_player_action(initialize_game_state(), move, player)

        self.assertIsInstance(board, np.ndarray)
        self.assertEqual(board.shape, (6,7))
        self.assertEqual(board[0, move], player) if move in np.arange(7)\
            else self.assertTrue(np.array_equal(board, np.zeros((6, 7))))

        #apply move in the same column to see if pieces stack within column:
        board = apply_player_action(board, move, player)
        self.assertEqual(board[0,move], board[1,move], player)
        #test whether appropriate Exceptions are raised:
        board[:, move] = np.ones(6)*player

        with self.assertRaises(ColumnError):
            apply_player_action(board, move, player)

        illegalMove = 8 #illegal move should raise Exception

        with self.assertRaises(BoardError):
            apply_player_action(board, illegalMove, player)


    def testInitializeGameState(self):

        board = initialize_game_state()

        self.assertIsInstance(board, np.ndarray)
        self.assertEqual(board.dtype, BoardPiece)
        self.assertTrue(np.array_equal(board, np.zeros((6, 7))))

    def testCheckEndState(self):

        from agents.common import check_end_state

        #Initilize two different boards:

        board = np.zeros((6, 7))
        board[0,0] = 1*player

        self.assertEqual(check_end_state(board, player), GameState.STILL_PLAYING)
        self.assertEqual(check_end_state(board, PLAYER2), GameState.STILL_PLAYING)

        board[:, 3] = np.ones(6)*player #is win for player
        board2 = board.copy()
        board2[:4, 3] = np.zeros(4) #player is no longer winning

        self.assertEqual(check_end_state(board, player), GameState.IS_WIN)
        self.assertEqual(check_end_state(board.T, player), GameState.IS_WIN) #checks function for row wins
        self.assertNotEqual(check_end_state(board, PLAYER2), GameState.IS_WIN) #player2 not winning
        self.assertEqual(check_end_state(board2, player), check_end_state(board2, player))
        self.assertEqual(check_end_state(board2, player), GameState.STILL_PLAYING)


        #Check whether the function also works for diagonal wins:

        board2[:4,:4] = np.eye(4)*PLAYER2 #is win for player2

        self.assertEqual(check_end_state(board2, PLAYER2), GameState.IS_WIN)

    def testConnectedFour(self):

        from agents.common import connected_four

        board = np.zeros((6, 7))
        board[0,0] = 1*player
        board2 = board.copy()

        self.assertFalse(connected_four(board, player))
        self.assertFalse(connected_four(board, PLAYER2))

        #Generate new board:
        board[:, 1] = np.ones(6)*player

        self.assertTrue(connected_four(board, player))
        self.assertFalse(connected_four(board2, player))
        self.assertTrue(connected_four(board.T, player))

        #Generate new board:
        board2[2:6,3:7] = np.eye(4)*PLAYER2
        board2[5,:] = np.array([1,1,1,0,1,1,1])*player

        self.assertFalse(connected_four(board2, player))
        self.assertFalse(connected_four(board2, player)) #Top corner piece is now player


    def testPrettyPrintBoard(self):

        from agents.common import pretty_print_board, string_to_board

        board1 = np.ones((6,7))
        board1[1:,2:] = np.zeros((5,5))*player
        board2 = np.zeros((6,7))
        board2[:4,:4] = np.eye(4)*PLAYER2
        board3 = initialize_game_state()
        board3[0,0] = player #checks that (0,0) is bottom left corner

        #representation of empty board:
        str0 = '|===============================|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|===============================|\n' \
               '|\t0\t1\t2\t3\t4\t5\t6\t|\n'

        #representation of board1:
        str1 = '|===============================|\n' \
               '|\tX\tX\t \t \t \t \t \t|\n' \
               '|\tX\tX\t \t \t \t \t \t|\n' \
               '|\tX\tX\t \t \t \t \t \t|\n' \
               '|\tX\tX\t \t \t \t \t \t|\n' \
               '|\tX\tX\t \t \t \t \t \t|\n' \
               '|\tX\tX\tX\tX\tX\tX\tX\t|\n' \
               '|===============================|\n' \
               '|\t0\t1\t2\t3\t4\t5\t6\t|\n'

        #representation of board2:
        str2 ='|===============================|\n' \
              '|\t \t \t \t \t \t \t \t|\n' \
              '|\t \t \t \t \t \t \t \t|\n' \
              '|\t \t \t \tO\t \t \t \t|\n' \
              '|\t \t \tO\t \t \t \t \t|\n' \
              '|\t \tO\t \t \t \t \t \t|\n' \
              '|\tO\t \t \t \t \t \t \t|\n' \
              '|===============================|\n' \
              '|\t0\t1\t2\t3\t4\t5\t6\t|\n'

        #representation of board3:
        str3 = '|===============================|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\t \t \t \t \t \t \t \t|\n' \
               '|\tX\t \t \t \t \t \t \t|\n' \
               '|===============================|\n' \
               '|\t0\t1\t2\t3\t4\t5\t6\t|\n'

        self.assertEqual(pretty_print_board(initialize_game_state()), str0)
        self.assertEqual(pretty_print_board(board1), str1)
        self.assertEqual(pretty_print_board(board2), str2)
        self.assertEqual(pretty_print_board(board3), str3)


    def testStringtoBoard(self):

        from agents.common import string_to_board, pretty_print_board

        #It's enough to check that string_to_board ° pretty_print = id:
        board = np.random.choice([player, PLAYER2], ((6,7)))
        self.assertTrue(np.array_equal(board, string_to_board(pretty_print_board(board))))


if __name__ == '__main__':
    unittest.main()


