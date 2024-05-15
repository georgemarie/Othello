import pygame

from .board import Board
from .constants import BLACK, SQUARE_SIZE, WHITE
from .disk import Disk


class GameController:
    def __init__(self, window):
        self._init()
        self.window = window
        # detect if both players can't make a move
        self.unmoved = 0

    def update(self):
        self.board.draw(self.window)
        self.get_valid_moves()
        self.draw_valid_moves(self.valid_moves)

        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = set()

    def get_valid_moves(self):
        self.valid_moves = self.board.get_moves(self.turn)

    def winner(self):
        return self.board.winner(self.unmoved)

    def reset(self):
        self._init()

    def select(self, row, col):
        move = (row, col)
        if move in self.valid_moves:
            self.board.insert_piece(row,  col, self.turn)
            # flip the turn
            self.change_turn()

    def draw_valid_moves(self, moves):
        # if a player has not moves i switch to the other player
        if(moves == set()):
            self.change_turn()
            self.unmoved += 1
            return

        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, self.turn, (col * SQUARE_SIZE + SQUARE_SIZE//2,
                                                        row * SQUARE_SIZE + SQUARE_SIZE//2), 40, width=1)
        self.unmoved = 0

    def change_turn(self):
        """changing turn between opponents"""
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def get_board(self):
        return self.board

    def ai_move(self, newState):
        self.board = newState
        print("evaluation = ", end='')
        print(self.board.evaluate())
        self.change_turn()
