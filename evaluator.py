#!/usr/bin/python

import numpy as np
import random as rnd

# A class for raising invalid move exceptions
class InvalidMove(Exception):
    """Raise an Invalid Move Exception"""

class Breakthrough:
    def __init__(self, board_size=8):
        self.board = np.zeros((board_size, board_size))

        self.board[:2, :] = 2
        self.board[board_size-2:, :] = 1

        # Player 1's direction is upwards (-1) and player 2's direction is downwards (+1)
        self.direction = [0, -1, 1]

        print(self.board)

        # Number of pieces captured so far by each player.
        # The first element is just for padding.
        self.captured = [0, 0, 0]

        self.player = None      # The player whose turn it is now.


    def next_player(self):
        # The other player.
        return 3 - self.player


    def is_legal_move(self, move):
        """Is this move a legal move?"""
        from_x, from_y = move[0]
        to_x, to_y = move[1]

        # First check if the piece we are trying to move the player's piece.
        if self.board[from_x, from_y] != self.player:
            raise InvalidMove("You can only move your own piece!")

        # First let's make sure that the change in y position is as per the rules.
        if to_y - from_y != self.direction[self.player]:
            raise InvalidMove("You have to vertically move exactly one unit in the player's direction!")

        # Now, we need to consider the horizontal displacement and the piece in the to_pos.
        to_piece = self.board[to_x, to_y]

        # if there is no horizontal displacement.
        if from_x == to_x:
            if to_piece != 0:   # the position is not empty.
                raise IvalidMove("You can't move to an occupied slot!")
            else:
                # This is just a vertical move.
                return 1

        # if there is horizontal displacement, check that it is just one slot to the right/left.
        if abs(from_x - to_x) > 1:
            raise InvalidMove("You can't move that far!")

        # At this point, we are in a diagonal move. Just check if the piece is the opposite player's.
        if to_piece != self.next_player():
            raise InvalidMove("You can only capture your opponent's piece!")

        # Now we are in a capturing move.
        return 2


    def is_pos_empty(self, pos):
        """Is this board position empty?"""
        return self.board[pos] == 0


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

                print(self.board)

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
