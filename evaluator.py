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

        # Pieces captured so far.
        self.captured = [0, 0]


    def alt_player(self, player):
        # The other player.
        return 3 - player

    def is_legal_move(self, move, player):
        from_pos = move[0]
        to_pos = move[1]

        if self.board[from_pos] != player:
            raise InvalidMove("Not Player's Piece!")

        if self.is_pos_empty(to_pos):
            if self.is_legal_move_vert(player, from_pos, to_pos):
                return 1
            else:
                raise InvalidMove("Invalid Move.!")

        else:
            if self.is_pos_alt_player(to_pos, player) and self.is_legal_move_diag(player, from_pos, to_pos):
                return 2
            raise("Invalid Move!")

    def is_pos_empty(self, pos):
        return self.board[pos] == 0

    def is_pos_alt_player(self, pos, player):
        return ( self.board[pos] != 0 ) and ( self.board[pos] != player )

    def is_legal_move_vert(self, player, from_pos, to_pos):
        if player == 1:
            # Assuming player 1's side is the bottom-most row
            return (from_pos[0] == to_pos[0]) and (to_pos[1] - from_pos[1] == 1)
        return (from_pos[0] == to_pos[0]) and (from_pos[1] - to_pos[1] == 1)

    def is_legal_move_diag(self, player, from_pos, to_pos):
        # x-coordinate may change 1 unit to the left or right.
        # the y-coordinate should change one unit in the player's direction.
        if player == 1:
            return (abs(from_pos[0] - to_pos[0]) == 1) and (to_pos[1] - from_pos[1] == 1)

        return (abs(from_pos[0] - to_pos[0]) == 1) and (from_pos[1] - to_pos[1] == 1)

    def do_move(self, move, player):
        move_type = self.is_legal_move(move, player)

        from_pos, to_pos = move

        # No matter what the move is, we have to empty the from_pos.
        self.board[from_pos] = 0

        # Also, the to_pos would now hold the player's piece.
        self.board[to_pos] = player

        capture = 0
        if move_type == 2:
            # Diagonal move

            # Captured player
            capture = alt_player(player)
            self.captured[capture - 1] += 1

        return self.game_ends(), capture

    def game_ends(self):
        """If the game has ended, return the winner's id (1 or 2).
        If the game has ended in a draw, return 0. Otherwise, return None.
        """
        pass
