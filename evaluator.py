#!/usr/bin/python

import numpy as np
import random as rnd

# A class for raising invalid move exceptions
class InvalidMove(Exception):
    """Raise an Invalid Move Exception"""


# A class for keeping track of players' scores
class PlayerScore():
    def __init__(self, obj=None, id=None, score=0):
        self.obj = obj          # The object representing the player.
        self.id = id
        self.score = score


class Breakthrough:
    def __init__(self, board_size=8):
        self.board = np.zeros((board_size, board_size), dtype=np.uint8)

        # store the board-size
        self.board_size = board_size

        # Player 1's direction is upwards (-1) and player 2's direction is downwards (+1)
        self.direction = [0, -1, 1]


    def reset(self):
        # Reset the board.
        self.board[:2, :] = 2
        self.board[self.board_size-2:, :] = 1

        self.board[2:self.board_size-2, :] = 0

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

        # First check if the piece we are trying to move is the player's piece.
        if self.board[from_x, from_y] != self.player:
            raise InvalidMove("You can only move your own piece!")

        # First let's make sure that the change in y position is as per the rules.
        if to_x - from_x != self.direction[self.player]:
            raise InvalidMove("You have to vertically move exactly one unit in the player's direction!")

        # Now, we need to consider the horizontal displacement and the piece in the to_pos.
        to_piece = self.board[to_x, to_y]

        # if there is no horizontal displacement.
        if from_y == to_y:
            if to_piece != 0:   # the position is not empty.
                raise IvalidMove("You can't move to an occupied slot!")
            else:
                # This is just a vertical move.
                return 1

        # if there is horizontal displacement, check that it is just one slot to the right/left.
        if abs(from_y - to_y) > 1:
            raise InvalidMove("You can't move that far!")

        # At this point, we are in a diagonal move.
        if to_piece ==0:        # the target slot is empty.
            return 2
        elif to_piece != self.next_player():
            raise InvalidMove("You can only capture your opponent's piece!")
        else: # Now we are in a capturing move.
            return 3


    def is_pos_empty(self, pos):
        """Is this board position empty?"""
        return self.board[pos] == 0


    def do_move(self, move):
        """Perform the move if it is legal."""
        # It is possible that the move may be None
        # It means that the current player has no move. Do nothing in that case.
        if not move:
            return False, False

        move_type = self.is_legal_move(move)

        from_pos, to_pos = move

        # No matter what the move is, we have to empty the from_pos.
        self.board[from_pos] = 0

        # Also, the to_pos would now hold the player's piece.
        self.board[to_pos] = self.player

        capture = False
        if move_type == 3:
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


    def evaluate_two(self, player1, player2):
        """Play the game using two agents. The agents are expected to be the objects of
        the Player class. Scoring: if a player returns an invalid move, or
        exceeds the time limit, his/her will get a 0 points and any of his/her
        previous wins will be forgotten. In that case, the opponent will get 1 point for the game.
        In a normal game, the winner will get 2 points per game.
        """

        pl = [None, player1, player2] # A list to make it easier to alternate between two players.

        pl[1].obj.start(1)        # First player
        pl[2].obj.start(2)        # Second player

        self.reset()

        self.player = 1
        capture = 0
        move = None
        move_num = 0

        print("Player:", pl[1].id, "Move num: ", move_num, "Move: ", move )
        print(self.board)

        while True:
            move = pl[self.player].obj.next_move(move, capture)
            ends, capture = self.do_move(move)

            move_num += 1

            print("Player:", pl[self.player].id, "Move num: ", move_num, "Move: ", move )
            print(self.board)

            if ends:
                # Let both players know that the game has ended.
                pl[self.player].obj.finish(self.player, move, True, 2)
                pl[self.next_player()].obj.finish(self.player, move, True, 0)
                print(pl[self.player].id, "wins.")
                break
            else:
                self.player = self.next_player()

        # At this point, presumably we know who won. Update the scores.
        pl[self.player].score += 2
        return


if __name__ == '__main__':
    import sys, ast
    # For the time being, assume that there are only two players and that we are given the modules of both.
    code = ast.parse(open(sys.argv[1]).read())
    eval(compile(code, '', 'exec'))
    pl1 = PlayerScore(Player(8), "A", 0)

    code = ast.parse(open(sys.argv[2]).read())
    eval(compile(code, '', 'exec'))
    pl2 = PlayerScore(Player(8), "B", 0)

    breaktrough = Breakthrough()
    breaktrough.evaluate_two(pl1, pl2)
    print("Final score:\n Player {0}: {1}, Player {2}: {3}".format(pl1.id, pl1.score, pl2.id, pl2.score))
