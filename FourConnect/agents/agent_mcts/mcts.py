import numpy as np
import agents.common as cm
from agents.agent_mcts.node import Node
from agents.agent_mcts.state import State
from typing import Tuple, Optional

def generate_move(board: np.ndarray,
                       player: cm.BoardPiece,
                       saved_state: Optional[cm.SavedState]
    ) -> Tuple[cm.PlayerAction, Optional[cm.SavedState]]:

        gamestate = cm.check_end_state(board, player)
        current_state = State(board, player, gamestate, None)
        root = Node.make_root(current_state)
        cm.pretty_print_board(root.state.board)
        bestmove, _ = Node.mcts(root)

        return bestmove, saved_state



