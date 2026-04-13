# Minimax AI with alpha-beta pruning. Depth is configurable at instantiation.

from src.ai.base import AIPlayer
from src.connect4 import (
    get_valid_locations, is_terminal_node, winning_move,
    get_next_open_row, copy_board, drop_piece, score_position
)


class MinimaxAI(AIPlayer):
    def __init__(self, depth: int = 5):
        self.depth = depth

    @property
    def name(self) -> str:
        return f"Minimax(depth={self.depth})"

    def get_move(self, board, piece) -> int:
        opp_piece = 1 if piece == 2 else 2
        col, _ = self._minimax(board, self.depth, float("-inf"), float("inf"), True, piece, opp_piece)
        return col

    def _minimax(self, board, depth, alpha, beta, maximizing, my_piece, opp_piece):
        valid_locations = get_valid_locations(board)
        terminal = is_terminal_node(board)

        if terminal:
            if winning_move(board, my_piece):
                return (None, 10000000)
            elif winning_move(board, opp_piece):
                return (None, -10000000)
            else:
                return (None, 0)

        if depth == 0:
            return (None, score_position(board, my_piece))

        if maximizing:
            value = float("-inf")
            best_col = valid_locations[0]
            for col in valid_locations:
                row = get_next_open_row(board, col)
                temp_board = copy_board(board)
                drop_piece(temp_board, row, col, my_piece)
                new_score = self._minimax(temp_board, depth - 1, alpha, beta, False, my_piece, opp_piece)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (best_col, value)
        else:
            value = float("inf")
            best_col = valid_locations[0]
            for col in valid_locations:
                row = get_next_open_row(board, col)
                temp_board = copy_board(board)
                drop_piece(temp_board, row, col, opp_piece)
                new_score = self._minimax(temp_board, depth - 1, alpha, beta, True, my_piece, opp_piece)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (best_col, value)
