# AI that picks the highest-scoring column using the heuristic function
# directly, with no lookahead. One step above random, one step below minimax.

from src.ai.base import AIPlayer
from src.connect4 import (
    get_valid_locations, get_next_open_row, copy_board,
    drop_piece, score_position
)


class GreedyAI(AIPlayer):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "Greedy"

    def get_move(self, board, piece) -> int:
        valid_locations = get_valid_locations(board)
        best_score = float("-inf")
        best_col = valid_locations[0]

        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        self.nodes_evaluated = len(valid_locations)
        self.last_score = best_score
        return best_col
