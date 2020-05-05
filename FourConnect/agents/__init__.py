import numpy as np
from agents.common import *

def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:

    # Randomly select a column to play:

    #action = np.random.randint(7)

    # Check if the field of the column is empty:

    action = 3

    if board[-1, action] == noPlayer:

        return action, saved_state if board[-1, action] == noPlayer \
                else generate_move_random(board, player, saved_state)