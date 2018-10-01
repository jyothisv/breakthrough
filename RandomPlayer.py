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
        self.board[board_size-2:, :] = 1

        self.board[2:board_size-2, :] = 0


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
        capture_moves = []
        vert_moves = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == self.player:
                    # It's our piece. Try to find if any capture move is possible.
                    from_pos = (i, j)
                    for to_pos in get_capture_pos(from_pos):
                        capture_moves.append((from_pos, to_pos))

                    # Now find out vertical moves.
                    for to_pos in get_vert_pos(from_pos):
                        vert_moves((from_pos, to_pos))

        if capture_moves:
            return rnd.choice(capture_moves)
        return rnd.choice(vert_moves)


    def get_capture_moves(from_pos):
        moves = []
        x, y = from_pos
        to_pos1 = (x-1, y + self.direction)
        to_pos2 = (x+1, y + self.direction)

        if self.board[to_pos1] == self.other_player:
            moves.append(to_pos1)

        if self.board[to_pos2] == self.other_player:
            moves.append(to_pos2)

        return moves


    def get_vert_moves(from_pos):
        moves = []
        x, y = from_pos
        to_pos = (x, y + self.direction)

        if self.board[ to_pos ] == 0: # if the target board position is empty.
            moves.append(to_pos)
        return moves


    def finish(self, player, move):
        """We know the player who won and the winning move."""
        pass
