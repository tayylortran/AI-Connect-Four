# Abstract base class for all AI players. Every AI must implement get_move,
# which takes the current board and the AI's piece and returns a column (0-6).

from abc import ABC, abstractmethod


class AIPlayer(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_move(self, board, piece) -> int:
        pass
