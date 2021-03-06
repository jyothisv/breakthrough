#!/usr/bin/python

import numpy as np
import random as rnd
import time
from itertools import permutations

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
    def __init__(self, board_size=8, timeout=2):
        self.board = np.zeros((board_size, board_size), dtype=np.uint8)

        # store the board-size
        self.board_size = board_size

        # Player 1's direction is upwards (-1) and player 2's direction is downwards (+1)
        self.direction = [0, -1, 1]

        self.timeout = timeout  # in seconds

        self.start_time = None


    def set_start_time(self):
        self.start_time = time.time()


    def check_timeout(self):
        if time.time() - self.start_time > self.timeout:
            raise InvalidMove("Timeout!")


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
        # It should not happen because in Breakthrough, draw is not possible.
        if not move:
            raise InvalidMove("Move cannot be None.")

        move_type = self.is_legal_move(move)

        from_pos, to_pos = move

        # No matter what the move is, we have to empty the from_pos.
        self.board[from_pos] = 0

        # Also, the to_pos would now hold the player's piece.
        self.board[to_pos] = self.player

        if move_type == 3:
            # Number of pieces that self.player captures is incremented.
            self.captured[self.player] += 1

        return self.game_ends()


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

        self.reset()

        self.player = 1
        capture = 0
        move = None
        move_num = 0

        print("Player:", pl[1].id, "Move num: ", move_num, "Move: ", move )
        print(self.board)


        try:
            self.set_start_time()
            pl[self.player].obj.start(1)        # First player
            self.check_timeout()

            self.player = self.next_player() # Now we are going to the second player.
            self.set_start_time()
            pl[2].obj.start(2)        # Second player
            self.check_timeout()

            self.player = self.next_player() # Again going back to the first player.
            while True:
                self.set_start_time()
                move = pl[self.player].obj.next_move(move)
                self.check_timeout()
                ends = self.do_move(move)

                move_num += 1

                print("Player:", pl[self.player].id, "Move num: ", move_num, "Move: ", move )
                print(self.board)

                if ends:
                    # Update the score.
                    pl[self.player].score += 2

                    print(pl[self.player].id, "wins.")
                    break
                else:
                    self.player = self.next_player()
        except InvalidMove as e:
            # The current player (self.player) must have made an invalid move. Penalize!
            # Give 1 point to the other player.
            pl[self.next_player()].score += 1

            print(e)            # Print the Exception.

        except:
            # Some other error. Again, penalize the current player.
            print("Runtime error!")
            pl[self.next_player()].score += 1



    def evaluate(self, players):
        """Play players against each other. Each player will play 10 games against each
        other player. 5 games will be as the first player and other games will be the
        second player."""

        player_pairs = list( permutations(players, 2) ) * 5 # All possible pairs, with 5 copies each
        rnd.shuffle(player_pairs)                           # randomly shuffle the pairs

        for pl1, pl2 in player_pairs:
            print("Game Starts: Group {0} vs Group {1}".format(pl1.id, pl2.id))
            self.evaluate_two(pl1, pl2)
            print("Game Ends!")




if __name__ == '__main__':
    import sys, ast

    # Generate PlayerScore objects for each player
    players = []

    for fname in sys.argv[1:]:
        # print("fname=",fname)
        code = ast.parse(open(fname).read())
        eval(compile(code, '', 'exec'))
        group_name = fname.split("/")[-1].split(".")[0] # TODO: Do away with this hack.
        players.append( PlayerScore(Player(), group_name, 0) )

    # code = ast.parse(open(sys.argv[2]).read())
    # eval(compile(code, '', 'exec'))
    # pl2 = PlayerScore(Player(), "B", 0)

    breaktrough = Breakthrough(8, 2)
    breaktrough.evaluate(players)
    # print("Final score:\n Player {0}: {1}, Player {2}: {3}".format(pl1.id, pl1.score, pl2.id, pl2.score))

    print("Final scores:")
    for pl in players:
        print("Group {0}: {1}".format(pl.id, pl.score))
