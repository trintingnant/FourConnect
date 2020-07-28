import numpy as np
import unittest
import sys, os
import agents.common as cm
import copy as copy


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

class testNode(unittest.TestCase):


    def test_root(self):

        from agents.agent_mcts.node import Node
        from agents.agent_mcts.state import State

        player = cm.PLAYER1
        root_state = State.root_state(player)
        root = Node.make_root(root_state)
        self.assertIsNone(root.parent)
        self.assertTrue(root==root.last_node)
        self.assertEqual(root.node_won, 0)

    def test_leaf(self, numTests: int = 8):

        from agents.agent_mcts.node import Node
        from agents.agent_mcts.state import State

        players = [cm.PLAYER1, cm.PLAYER2, cm.noPlayer]
        end_states = [cm.GameState.IS_WIN, cm.GameState.IS_LOSS, cm.GameState.IS_DRAW]

        #Use fuzzing
        for player in players[:2]:
            for i in range(numTests):

                board = np.random.choice(players, (6, 7))
                test_state = State(board, player)
                test_node = Node(test_state, [], None, 0, 0, None, None)
                actually_leaf = cm.check_end_state(board, player) in end_states

                self.assertEqual(actually_leaf, Node.leaf(test_node))

    def test_depth(self):

        from agents.agent_mcts.node import Node
        from agents.agent_mcts.state import State

        player = cm.PLAYER1
        root_state = State.root_state(player)
        tree = Node.make_root(root_state)
        self.assertIsInstance(tree.depth(), int)
        self.assertEqual(tree.depth(), 0)

        #increase longest path:
        tree.children.append(copy.deepcopy(tree))
        self.assertEqual(tree.depth(), 1)

        #increase longest path by 2
        tree.children[0].children.append(copy.deepcopy(tree))
        self.assertEqual(tree.depth(), 3)

        #increase branching factor in root
        root2 = Node.make_root(root_state)
        tree.children.append(copy.deepcopy(root2))
        self.assertEqual(tree.depth(), 3)


    def test_select_and_expand(self):
        #tested in test_mcts
        pass

    def test_simulate_and_propagate(self):
        #tested in test_mcts
        pass

    def test_mcts(self):

        from agents.agent_mcts.node import Node
        from agents.agent_mcts.state import State

        players = [cm.PLAYER1, cm.PLAYER2, cm.noPlayer]


        for i in range(5):

            # Use fuzzing:
            player = np.random.choice(players[:2])
            numIters = np.random.choice(range(15))

            #Run mcts:
            root_state = State.root_state(player)
            tree = Node.make_root(root_state)
            tree.mcts(numIters)

            self.assertEqual(tree.node_reached, numIters) #tree root reached exactly numIters times
            #self.assertTrue(np.array([tree.node_reached > child.node_reached for child in tree.children]).all())
            self.assertTrue(tree.node_won <= numIters)


if __name__ == '__main__':
    unittest.main()
