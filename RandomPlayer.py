#!/usr/bin/python

import numpy as np
import random as rand

class Player:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size))
        self.board_size = board_size


    def start(self, player):
        """Start a new game."""
        self.player = player
        self.other_player = 3 - player

        # The vertical direction. Up = -1 and Down = +1
        if self.player == 1:
            self.direction = -1
        else:
            self.direction = 1

        # Reset the player's board.
        self.board[:2, :] = 2
        self.board[self.board_size-2:, :] = 1

        self.board[2:self.board_size-2, :] = 0


    def do_move(self, move):
        """Do the necessary book-keeping to keep track of the board position."""
        from_pos, to_pos = move
        self.board[from_pos] = 0

        # We only get the other player's move as an argument.
        self.board[to_pos] = self.other_player


    def next_move(self, move, capture):
        """Calculate the next move."""
        # As the random player, we just make one list of capture moves and another list of
        # vertical moves. If a capture is possible, we randomly pick one. If no capture
        # is possible, take a random vertical move.
        #
        # Note that the strategy and the implementation are just for illustrative purposes.
        # Both are meant to be improved.

        # First of all, apply the move from the previous player.
        if move:
            self.do_move(move)

        capture_moves = []
        vert_moves = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == self.player:
                    # It's our piece. Try to find if any capture move is possible.
                    from_pos = (i, j)
                    print("from pos = ", from_pos, "piece = ", self.board[i, j])
                    for to_pos in self.get_capture_pos(from_pos):
                        capture_moves.append((from_pos, to_pos))

                    # Now find out vertical moves.
                    for to_pos in self.get_vert_pos(from_pos):
                        vert_moves.append((from_pos, to_pos))

        print("player = ", self.player, "capture_moves =", capture_moves, "vert_moves = ", vert_moves)

        our_move = None

        if capture_moves:
            our_move = rnd.choice(capture_moves)
        else:
            our_move = rnd.choice(vert_moves)

        # Before passing on the move, apply the move to our own board.
        self.do_move(our_move)
        return our_move


    def get_capture_pos(self, from_pos):
        moves = []
        x, y = from_pos
        to_pos1 = (x + self.direction, y - 1)
        to_pos2 = (x + self.direction, y + 1)

        if self.within_bounds_pos( to_pos1 ) and self.board[to_pos1] == self.other_player:
            moves.append(to_pos1)

        if self.within_bounds_pos( to_pos2 ) and self.board[to_pos2] == self.other_player:
            moves.append(to_pos2)

        return moves


    def get_vert_pos(self, from_pos):
        moves = []
        x, y = from_pos
        to_pos = (x + self.direction, y)

        print(from_pos, to_pos)

        if self.within_bounds_pos( to_pos ) and self.board[ to_pos ] == 0: # if the target board position is empty.
            moves.append(to_pos)
        return moves


    def within_bounds_pos(self, pos):
        x, y = pos
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def finish(self, player, move):
        """We know the player who won and the winning move."""
        pass
