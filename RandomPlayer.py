#!/usr/bin/python

import numpy as np
import random as rand

class Player:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size), dtype=np.uint8)
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


    def do_move(self, move, player):
        """Do the necessary book-keeping to keep track of the board position."""
        if move:                # move may be None.
            from_pos, to_pos = move
            self.board[from_pos] = 0

            # Which player's move was it?
            self.board[to_pos] = player


    def next_move(self, move, capture):
        """Calculate the next move."""
        # As the random player, we just make one list of capture moves and another list of
        # vertical moves. If a capture is possible, we randomly pick one. If no capture
        # is possible, take a random vertical move.
        #
        # Note that the strategy and the implementation are just for illustrative purposes.
        # Both are meant to be improved.

        # First of all, apply the move from the previous player.
        self.do_move(move, self.other_player)

        capture_moves = []
        vert_diag_moves = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == self.player:
                    # It's our piece. Try to find if any capture move is possible.
                    from_pos = (i, j)

                    valid_moves = self.get_valid_pos(from_pos)

                    for to_pos in valid_moves[0]:
                        vert_diag_moves.append( (from_pos, to_pos) ) # Add the returned vert_diag_moves to the list

                    for to_pos in valid_moves[1]:
                        capture_moves.append( (from_pos, to_pos) )   # Similarly, add the returned captured moves.

        # print("player = ", self.player, "capture_moves =", capture_moves, "vert_moves = ", vert_moves)

        our_move = None

        if capture_moves:
            our_move = rnd.choice(capture_moves)
        elif vert_diag_moves:
            our_move = rnd.choice(vert_diag_moves)

        # Before passing on the move, apply the move to our own board.
        self.do_move(our_move, self.player)
        return our_move


    def get_valid_pos(self, from_pos):
        x, y = from_pos

        capture_moves = []
        vert_diag_moves = []

        to_pos = (x + self.direction, y) # Possible vertical move

        if self.within_bounds_pos( to_pos ) and self.board[ to_pos ] == 0: # if the target board position is empty.
            vert_diag_moves.append( to_pos )


        for to_pos in [ (x + self.direction, y - 1), (x + self.direction, y + 1) ]: # Possible diagonal moves
            if self.within_bounds_pos( to_pos ):
                if self.board[ to_pos ] == 0: # if the target board position is empty.
                    vert_diag_moves.append( to_pos )
                elif self.board[ to_pos ] == self.other_player:
                    capture_moves.append( to_pos )
        return vert_diag_moves, capture_moves


    def within_bounds_pos(self, pos):
        x, y = pos
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def finish(self, player, move, valid, score):
        """We know the player who won and the winning move.
        The parameters are:
        1) player: the player who did the final move,
        2) move: the final move
        3) valid: whether the last move was valid.
        4) score: score that the current player gets as a result."""
        pass
