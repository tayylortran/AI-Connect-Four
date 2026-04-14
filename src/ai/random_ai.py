# AI that picks a random valid column. Used as a baseline.

import random
from src.ai.base import AIPlayer
from src.connect4 import get_valid_locations


class RandomAI(AIPlayer):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "Random"

    def get_move(self, board, piece) -> int:
        self.nodes_evaluated = 1
        self.last_score = 0
        return random.choice(get_valid_locations(board))
