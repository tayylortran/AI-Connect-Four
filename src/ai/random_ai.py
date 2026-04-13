# AI that picks a random valid column. Used as a baseline.

import random
from src.ai.base import AIPlayer
from src.connect4 import get_valid_locations


class RandomAI(AIPlayer):
    @property
    def name(self) -> str:
        return "Random"

    def get_move(self, board, piece) -> int:
        return random.choice(get_valid_locations(board))
