# Heuristic functions for Minimax. Each takes (board, piece) and returns a
# numeric score — higher is better for `piece`. Swap them into MinimaxAI to
# change play style without touching search logic.

from src.connect4 import ROWS, COLS, EMPTY, PLAYER_PIECE, AI_PIECE

WINDOW_LENGTH = 4


def _evaluate_window(window, piece, own_3_score, own_2_score, opp_3_penalty):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += own_3_score
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += own_2_score

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= opp_3_penalty

    return score


def _score_board(board, piece, center_bonus, own_3_score, own_2_score, opp_3_penalty):
    score = 0

    # Center column bonus
    center_array = [int(v) for v in board[:, COLS // 2]]
    score += center_array.count(piece) * center_bonus

    # Horizontal
    for r in range(ROWS):
        row_array = [int(v) for v in board[r, :]]
        for c in range(COLS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += _evaluate_window(window, piece, own_3_score, own_2_score, opp_3_penalty)

    # Vertical
    for c in range(COLS):
        col_array = [int(v) for v in board[:, c]]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += _evaluate_window(window, piece, own_3_score, own_2_score, opp_3_penalty)

    # Diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [int(board[r + i][c + i]) for i in range(WINDOW_LENGTH)]
            score += _evaluate_window(window, piece, own_3_score, own_2_score, opp_3_penalty)

    # Diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [int(board[r - i][c + i]) for i in range(WINDOW_LENGTH)]
            score += _evaluate_window(window, piece, own_3_score, own_2_score, opp_3_penalty)

    return score


def balanced_heuristic(board, piece):
    """Current default behavior — equal weight on offense and defense."""
    return _score_board(board, piece,
                        center_bonus=4,
                        own_3_score=8,
                        own_2_score=3,
                        opp_3_penalty=10)


def aggressive_heuristic(board, piece):
    """Prioritizes building its own threats over blocking the opponent.
    Easier to beat — it will sometimes ignore your winning threats."""
    return _score_board(board, piece,
                        center_bonus=6,
                        own_3_score=16,
                        own_2_score=6,
                        opp_3_penalty=4)


def defensive_heuristic(board, piece):
    """Prioritizes blocking the opponent over building its own threats.
    Harder to beat — it shuts down your setups before building its own."""
    return _score_board(board, piece,
                        center_bonus=4,
                        own_3_score=8,
                        own_2_score=3,
                        opp_3_penalty=20)
