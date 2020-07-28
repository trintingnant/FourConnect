import numpy as np
import unittest
import sys, os
import agents.common as cm
import copy as copy
from agents.agent_mcts.state import State

'''
Tests the functions from the State class
'''

#Block annoying prints from the pprint function:
def blockPrinting():
    sys.stdout = open(os.devnull, 'w')

def unblockPrinting():
    sys.stdout = sys.__stdout__

blockPrinting()
unblockPrinting()

board = cm.initialize_game_state()

class testState(unittest.TestCase):

    def test_root_state(self):
        player = cm.PLAYER1
        state = State.root_state(player)
        self.assertTrue(np.array_equal(np.zeros((6,7)), state.board))
        self.assertEqual(player, state.player)
        self.assertEqual(state.gamestate, cm.GameState.STILL_PLAYING)
        self.assertIsNone(state.lastMove)

    def test_perform_move(self):

        board = cm.initialize_game_state()
        player = cm.PLAYER1
        possible_moves = np.arange(7)
        state = State(board, player)
        self.assertEqual(state.gamestate, cm.GameState.STILL_PLAYING)
        self.assertTrue(np.array_equal(state.board, cm.initialize_game_state()))

        #Test for all possible moves
        #All other functionality tested in tests_common

        for move in possible_moves:

            new_state = copy.deepcopy(state).perform_move(move)

            self.assertEqual(new_state.lastMove, move) #check that lastMove updates properly
            self.assertEqual(new_state.player, cm.PLAYER2) #check that players are alternating
            self.assertEqual(np.count_nonzero(new_state.board), 1) #check that only one piece is played
            self.assertEqual(new_state.gamestate, cm.GameState.STILL_PLAYING) #check that gamestate updates properly

if __name__ == '__main__':
    unittest.main()
