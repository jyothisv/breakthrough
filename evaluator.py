#!/usr/bin/python

import numpy as np

# A class for raising invalid move exceptions
class InvalidMove(Exception):
    """Raise an Invalid Move Exception"""

class Breakthrough:
    def __init__(self, board_size=8):
        self.board = np.zeros((board_size, board_size))

        print(self.board)

        self.board[:2, :] = 2
        self.board[board_size-2:, :] = 1

        # Number of pieces captured so far.
        self.captured = [0, 0]

        self.player = None      # The player whose turn it is now.


    def next_player(self):
        # The other player.
        return 3 - self.player


    def is_legal_move(self, move):
        from_pos = move[0]
        to_pos = move[1]

        if self.board[from_pos] != self.player:
            raise InvalidMove("Not Player's Piece!")

        if self.is_pos_empty(to_pos):
            if self.is_legal_move_vert(from_pos, to_pos):
                return 1
            else:
                raise InvalidMove("Invalid Move.!")

        else:
            if self.is_pos_next_player(to_pos) and self.is_legal_move_diag(from_pos, to_pos):
                return 2
            raise("Invalid Move!")


    def is_pos_empty(self, pos):
        """Is this board position empty?"""
        return self.board[pos] == 0


    def is_pos_next_player(self, pos):
        """Does this board position belong to the other player?"""
        return ( self.board[pos] != 0 ) and ( self.board[pos] != self.player )


    def is_legal_move_vert(self, from_pos, to_pos):
        """Is it a legal vertical move?"""
        if self.player == 1:
            # Assuming player 1's side is the bottom-most row
            return (from_pos[0] == to_pos[0]) and (to_pos[1] - from_pos[1] == 1)
        return (from_pos[0] == to_pos[0]) and (from_pos[1] - to_pos[1] == 1)

    def is_legal_move_diag(self, from_pos, to_pos):
        """Is it a legal diagonal move?"""
        # x-coordinate may change 1 unit to the left or right.
        # the y-coordinate should change one unit in the player's direction.
        if self.player == 1:
            return (abs(from_pos[0] - to_pos[0]) == 1) and (to_pos[1] - from_pos[1] == 1)

        return (abs(from_pos[0] - to_pos[0]) == 1) and (from_pos[1] - to_pos[1] == 1)


    def do_move(self, move):
        """Perform the move if it is legal."""
        move_type = self.is_legal_move(move)

        from_pos, to_pos = move

        # No matter what the move is, we have to empty the from_pos.
        self.board[from_pos] = 0

        # Also, the to_pos would now hold the player's piece.
        self.board[to_pos] = self.player

        capture = 0
        if move_type == 2:
            # Diagonal move

            # Captured player
            capture = next_player(self.player)
            self.captured[capture - 1] += 1

        return self.game_ends(), capture


    def game_ends(self):
        """If the game has ended, return the winner's id (1 or 2).
        If the game has ended in a draw, return 0. Otherwise, return None.
        """
