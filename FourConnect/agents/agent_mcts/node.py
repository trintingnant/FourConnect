import numpy as np
import agents.common as cm
from agents.agent_mcts.state import State
from typing import List, Union, Tuple
import copy as copy


class Node:

    def __init__(self,
                 state: State,
                 children: List['Node'],
                 parent: 'Node',
                 node_reached: int,
                 node_won: int,
                 move: cm.PlayerAction,
                 last_node: 'Node'):

        '''
        Node class for keeping track of the score of a gamestate
        the programme walks down the tree and propagates scores
        from terminal leaves upwards
        :param state: the game state (cf. state.py)
        :param children: the node's children
        :param parent: the node's parent node
        :param node_reached: nTimes the node has been visited
        :param node_won: nTimes a simulation starting from the node won
        :param last_node: the last expanded node in the entire tree
        '''

        self.state = state
        self.children = children
        self.parent = parent
        self.node_reached = node_reached
        self.node_won = node_won
        self.last_node = last_node,
        self.move = move

    #Getter and setter methods for class attributes:

    def set_state(self, state):
        self.state = state
        return self

    def get_state(self, state):
        return self.state

    def set_children(self, children: List['Node']):
        self.children = children
        return self

    def get_children(self):
        return self.children

    def set_parent(self, parent: 'Node'):
        self.parent = parent
        return self

    def get_parent(self):
        return self.parent

    def set_node_reached(self, nTimes: int):
        self.node_reached = nTimes
        return self

    def increment_node_reached(self):
        self.node_reached += 1
        return self

    def get_node_reached(self):
        return self.node_reached

    def set_node_won(self, nTimes: int):
        self.node_won = nTimes
        return self

    def increment_node_won(self):
        self.node_won += 1
        return self

    def get_node_won(self):
        return self.node_won

    def set_last_node(self, node: 'Node'):
        self.last_node = node
        return self

    def get_last_node(self):
        return self.last_node

    def get_move(self):
        return self.move

    def set_move(self, move):
        self.move = move
        return self

    def get_grandparent(self):
        if self.parent is None:
            return None
        else:
            return self.parent.parent

    def get_child(self, numChild: np.int8):
        return self.get_children()[numChild]

    def set_child(self, numChild: np.int8, child: 'Node'):
        '''
        Resets a specific child of a given node
        :param numChild: the child to be replaced
        :param child: the new subtree to append to the given node
        :return: a new tree
        '''

        self.children[numChild] = child
        return self

    #Helper methods:

    @staticmethod
    def make_root(state: State) -> 'Node':
        '''
        Generates a root tree
        :param state: the root state (e.g. initialise_game_board())
        :return: The root of the game tree
        '''
        root = Node(state, [], None, 0, 0, None, None)
        root.set_last_node(root)
        return root

    def depth(self) -> int:
        '''
        Returns depth of a tree
        :return: the depth of the tree
        '''

        if len(self.children) == 0:
            return 0

        else:
            child_depths = np.array([child.depth() for child in self.children])
            depth = 1 + child_depths.max()
            return depth

    def leaf(self):

        '''
        Checks if the state is a terminal state
        :return: bool := is the state a terminal state?
        '''
        bool = (cm.check_end_state(self.state.board, self.state.player)\
                    in [cm.GameState.IS_WIN, cm.GameState.IS_LOSS])
        return bool

    def ucb(self, eps=np.sqrt(2)) -> Union[float, None]:
        '''
        Computes upper confidence bound for a given node
        :param eps: exploration parameter
        :return:
        '''
        if self.node_reached == 0:
            return 0
        if self.node_won == 0:
            return 0
        if self.get_parent().node_reached == 0:
            return 0
        if self.parent is None:
            return 0

        else:
            exploit = self.get_node_won() / self.get_node_reached()
            explore = eps * np.sqrt(np.log(self.parent.get_node_reached()) / self.get_node_reached())
            return explore + exploit

    #MCTS: Monte Carlo Tree Search

    def select_and_expand(self) -> Tuple['Node', 'Node']:
        '''
        Runs the first two phases of the MCTS algorithm
        Selects and expands a node in the search tree
        :return: a tree expanded by one node
        '''

        expanded_node = None

        possible_moves, *_ = np.where(self.state.board[5] == cm.noPlayer)
        lastMoves = np.array([child.state.lastMove for child in self.children])
        unexpanded_nodes = np.array([move for move in possible_moves if move not in lastMoves])

        # if not all expanded -> expand one of the unexpanded children
        if len(unexpanded_nodes) != 0:
            self.increment_node_reached()
            # Expand random child
            move = np.random.choice(unexpanded_nodes)  # Phase 1: Selection
            new_state = copy.deepcopy(self.state.perform_move(move))
            expanded_node = Node(new_state, [], self, 1, 0, None, move)  # node_reached == 1, node_won == 0
            self.children.append(expanded_node)  # Phase 2: Expansion
            self.set_last_node(expanded_node)
            return self, expanded_node


        else:

            self.increment_node_reached()
            children_ucb = np.array([child.ucb() for child in self.children])
            expand_child = children_ucb.argmax()  # select child with best score
            last_move_parent = self.get_child(expand_child).state.lastMove
            selected_child = copy.deepcopy(self.get_child(expand_child))
            return selected_child.select_and_expand() # recursive call to subtree := expand by one
            #self.set_child(expand_child, selected_child)  # append to tree
            #selected_child.set_state(selected_child.state.set_lastMove(last_move_parent))


    def simulate_and_propagate(self, last_node: 'Node') -> 'Node':
        '''
        Runs the third and fourth stage of the MCTS algorithm.
        Simulates a game from a given node, until a leaf is reached.
        Then propagates the result up the game tree.
        :param self: the entire tree so far
        :return: The result of the simulated game
        '''

        #Phase 3: Simulate

        current_state = copy.deepcopy(last_node.state)
        #print('current_state: ', current_state.gamestate)

        #Check for terminal state
        while current_state.gamestate == cm.GameState.STILL_PLAYING:

                #cm.pretty_print_board(current_state.board)
                possible_moves, *_ = np.where(current_state.board[5] == cm.noPlayer)
                move = np.random.choice(possible_moves) #Pick random move
                current_state.perform_move(move) #Perform move
                current_state.update_gamestate()
                #print('current_state: ', current_state.gamestate, current_state.player)
                #cm.pretty_print_board(current_state.board)

        #cm.pretty_print_board(current_state.board)

        #Phase 4: Backpropagation:
        outcome, loosing_player = current_state.get_gamestate(), current_state.get_player()
        #print(outcome)
        #print(current_state.player)

        current_node = last_node

        if outcome == cm.GameState.IS_LOSS:
            while current_node is not None:
                #print(current_node.state.player)

                if current_node.state.get_player() != loosing_player: #player is winning player
                    current_node.increment_node_won()
                    current_node = current_node.get_parent()
                else:
                    current_node = current_node.get_parent()

        #print(np.array([child.node_won for child in self.children]))
        #print(np.array([child.node_reached for child in self.children]))
        #print(self.node_won)

        return self


    def mcts(self, numIters: int=10):
        '''
        Sucessively expands the game tree to get an estimate of value function
        :param numIters: number of node to expand
        :return:
        '''

        #current_tree = self
        #current_tree = current_tree.simulate_and_propagate() #Simulation for root node

        for i in range(numIters):

            _, last_node = self.select_and_expand()
            self.simulate_and_propagate(last_node)

        print(self.node_reached)
        children_ucb = np.array([child.ucb() for child in self.children])
        moves = np.array([child.state.lastMove for child in self.children])
        bestmove = moves[np.argmax(children_ucb)]

        return bestmove, self























































