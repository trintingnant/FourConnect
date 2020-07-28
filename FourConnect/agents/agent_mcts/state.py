import numpy as np
import agents.common as cm
from typing import Optional
import copy as copy

class State:
    '''
    Class that bundles different attributes:
    :param: board: the current game board
    :param player: the current player
    :param lastMove: the last performed move
    '''

    def __init__(self,
                 board: np.ndarray,
                 player: cm.BoardPiece,
                 gamestate: cm.GameState = cm.GameState.STILL_PLAYING,
                 lastMove: Optional[cm.PlayerAction]=None):

        self.board = board
        self.player = player
        self.gamestate = gamestate
        self.lastMove = lastMove


    #Getter and setter methods:

    def set_board(self, board: np.ndarray):
        self.board = board
        return self

    def get_board(self):
        return self.board

    def set_player(self, player: cm.BoardPiece):
        self.player = player
        return self

    def get_player(self):
        return self.player

    def get_gamestate(self):
        return self.gamestate

    def set_lastMove(self, move: cm.PlayerAction):
        self.lastMove = move
        return self

    def update_gamestate(self):
        self.gamestate = cm.check_end_state(self.board, self.player)
        return self

    #Other methods:

    @staticmethod
    def root_state(player: cm.BoardPiece):
        '''
        Initializes starting state with starting player
        :param player: the starting player
        :return: the root state of the game
        '''
        return State(cm.initialize_game_state(), player, cm.GameState.STILL_PLAYING, None)

    def perform_move(self, move: cm.PlayerAction):

        new_board = cm.apply_player_action(self.board, move, self.player)
        self.set_board(new_board)
        self.set_lastMove(move)
        self.set_player(cm.PLAYER2) if self.player == cm.PLAYER1 else self.set_player(cm.PLAYER1)

        return self













