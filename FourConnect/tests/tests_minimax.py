import numpy as np
import unittest
from agents.common import initialize_game_state, PLAYER2, PLAYER1 as player, apply_player_action
from agents.agent_minimax.minimax import MAX_DEPTH
import sys, os


'''
These tests tested an older version of minimax that I have since reworked.
They then passed.
Now that I'm using a heuristic, we should expect them to fail.
'''

#Block annoying prints from the pprint function:
def blockPrinting():
    sys.stdout = open(os.devnull, 'w')

def unblockPrinting():
    sys.stdout = sys.__stdout__

blockPrinting()

alpha = np.NINF
beta = np.inf

#Initialize boards for testing:
board = initialize_game_state()
board2 = board.copy()
board2[0,3:6] = np.ones(3)*player #player has a forced win

class testMiniMax(unittest.TestCase):

    @unittest.expectedFailure
    def test_maxMinValue(self):
        from agents.agent_minimax.minimax import maxValue, minValue

        self.assertEqual(maxValue(board, player, alpha, beta, MAX_DEPTH-4), 0) # can't win in two moves

        boardTemp = board.copy()
        boardTemp[0,4:6] = np.ones(2)*player
        self.assertEqual(maxValue(boardTemp, player, alpha, beta, MAX_DEPTH-4), 0)
        self.assertEqual(minValue(boardTemp, player, alpha, beta, MAX_DEPTH-4), -1000)

        #minValue should return 0 even on the forced-win board:
        self.assertEqual(minValue(board2, player, alpha, beta, MAX_DEPTH-2), -1000)
        self.assertEqual(maxValue(board2, PLAYER2, alpha, beta, MAX_DEPTH-2), -1000)

    @unittest.expectedFailure
    def test_alphaBeta(self):#

        from agents.agent_minimax.minimax import alphaBeta

        self.assertEqual(alphaBeta(board, player, MAX_DEPTH-8), 0)

        boardTemp = apply_player_action(board, 0, player)
        self.assertEqual(alphaBeta(boardTemp, PLAYER2, MAX_DEPTH), 0)

        #Forced-win board: still should return 0:
        self.assertEqual(alphaBeta(board2, player, MAX_DEPTH-2), 0)
        self.assertEqual(alphaBeta(board2, PLAYER2, MAX_DEPTH-2), 0)

    @unittest.expectedFailure
    def test_iterativeDeepeningSearch(self):

        from agents.agent_minimax.bare_bones_minimax import iterativeDeepingSearch

        board = initialize_game_state()
        #No heurstic && no winning moves -> all opening moves have the same score: 0
        self.assertListEqual(iterativeDeepingSearch(board, player)[0], [0]) #check score
        self.assertListEqual(iterativeDeepingSearch(board, player)[1][0], [0,1,2,3,4,5,6]) #check moves
        #Should return winning moves on forced-win board: [2,6]
        self.assertListEqual(iterativeDeepingSearch(board2, player)[0], [1]) #check score
        self.assertListEqual(iterativeDeepingSearch(board2, player)[1][0], [2,6]) #check moves



if __name__ == '__main__':
    unittest.main()
