#!/usr/bin/python

import numpy as np
import random as rnd

# A class for raising invalid move exceptions
class InvalidMove(Exception):
    """Raise an Invalid Move Exception"""

class Breakthrough:
    def __init__(self, board_size=8):
        self.board = np.zeros((board_size, board_size))

        print(self.board)

        self.board[:2, :] = 2
        self.board[board_size-2:, :] = 1

        # Number of pieces captured so far by each player.
        # The first element is just for padding.
        self.captured = [0, 0, 0]

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

        capture = False
        if move_type == 2:
            capture = True
            # Number of pieces that self.player captures is incremented.
            self.captured[self.player] += 1

        return self.game_ends(), capture


    def game_ends(self):
        """If the game has ended, return the winner's id (1 or 2).
        If the game has ended in a draw, return 0. Otherwise, return None.
        A player wins if one of his/her pieces reaches the opposite end.
        Another way for a player to win is to capture all the pieces of the enemy.
        """
        if self.captured[self.player] == 2*self.board_size:
            return True

        target_row = 0
        if self.player == 2:
            target_row = self.board_size-1

        return sum( self.board[target_row, :] == self.player ) >= 1


    def evaluator(self, player1, player2, trials=5):
        """Play the game using two agents. The agents are expected to be the objects of
        the Player class. Scoring: if a player returns an invalid move, or
        exceeds the time limit, his/her will get a 0 points and any of his/her
        previous wins will be forgotten. In that case, the opponent will get 1 point for the game.
        In a normal game, the winner will get 2 points per game.
        """

        games = ( [True] * trials ) + ([False] * trials)
        rnd.shuffle(games)

        scores = [0, 0, 0]

        pl = [None, None, None]

        for game in games:
            if game:
                pl[1], pl[2] = player1, player2
            else:
                pl[1], pl[2] = player2, player1

            pl[1].start(1)        # First player
            pl[2].start(2)        # Second player

            self.player = 1
            capture = 0
            move = None
            while True:
                move = pl[self.player].next_move(move, capture)
                ends, capture = self.do_move(move)
                if ends:
                    # Let both players know that the game has ended.
                    pl[1].finish(self.player, move)
                    pl[2].finish(self.player, move)
                    break
                else:
                    self.player = self.next_player()

            # At this point, presumably we know who won. Update the scores.
            scores[self.player] += 2
        return scores
