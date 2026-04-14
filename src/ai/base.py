# Abstract base class for all AI players. Every AI must implement get_move,
# which takes the current board and the AI's piece and returns a column (0-6).

from abc import ABC, abstractmethod


class AIPlayer(ABC):
    def __init__(self):
        self.nodes_evaluated = 0
        self.last_score = 0

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_move(self, board, piece) -> int:
        """Return the chosen column and update nodes_evaluated and last_score."""
        pass
