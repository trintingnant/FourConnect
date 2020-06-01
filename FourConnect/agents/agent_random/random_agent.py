import numpy as np
from typing import Tuple, Optional
from agents.common import BoardPiece, noPlayer, PlayerAction, SavedState

def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:

    # Randomly select a column to play:
    action = np.random.randint(7)

    # Check if the last field of the column is empty:
    if board[-1, action] == noPlayer:
        return action, saved_state
    else:
        return generate_move_random(board, player, saved_state)
