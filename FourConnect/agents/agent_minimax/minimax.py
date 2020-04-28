import numpy as np


from agents.common import GameState




available_moves = np.arange(7)



def minValue (
        board: np.ndarray, state: GameState,
        alpha: float, beta: float, depth: int
        ) -> int:

        if depth == 0 or GameState != GameState.STILL_PLAYING:

            return state


        raise NotImplemented


def maxValue (board: np.ndarray) -> int:

    raise NotImplemented





