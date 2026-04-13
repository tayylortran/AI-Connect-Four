# This file will contain the core Connect Four game logic, including the board
# representation, move handling, and functions to check for wins or valid moves.

import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def copy_board(board):
    return board.copy()

def winning_move(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE) or
        winning_move(board, AI_PIECE) or
        len(get_valid_locations(board)) == 0
    )

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 8
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 10

    return score

def score_position(board, piece):
    score = 0

    center_array = [int(value) for value in board[:, COLS // 2]]
    score += center_array.count(piece) * 4

    for r in range(ROWS):
        row_array = [int(value) for value in board[r, :]]
        for c in range(COLS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLS):
        col_array = [int(value) for value in board[:, c]]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [int(board[r + i][c + i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [int(board[r - i][c + i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

TREE_VIZ_DEPTH = 3


class TreeNode:
    __slots__ = ('col', 'score', 'maximizing', 'pruned', 'children')

    def __init__(self, col, maximizing, score=None, pruned=False):
        self.col = col
        self.score = score
        self.maximizing = maximizing
        self.pruned = pruned
        self.children = []


def minimax(board, depth, alpha, beta, maximizing_player, node=None, _vd=0):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    if terminal:
        if winning_move(board, AI_PIECE):
            return (None, 10000000)
        elif winning_move(board, PLAYER_PIECE):
            return (None, -10000000)
        else:
            return (None, 0)

    if depth == 0:
        return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = float("-inf")
        best_col = valid_locations[0]
        for i, col in enumerate(valid_locations):
            child = None
            if node is not None and _vd < TREE_VIZ_DEPTH:
                child = TreeNode(col=col, maximizing=False)
                node.children.append(child)
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False, child, _vd + 1)[1]
            if child is not None:
                child.score = new_score
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                if node is not None and _vd < TREE_VIZ_DEPTH:
                    for pcol in valid_locations[i + 1:]:
                        node.children.append(TreeNode(col=pcol, maximizing=False, pruned=True))
                break
        return (best_col, value)
    else:
        value = float("inf")
        best_col = valid_locations[0]
        for i, col in enumerate(valid_locations):
            child = None
            if node is not None and _vd < TREE_VIZ_DEPTH:
                child = TreeNode(col=col, maximizing=True)
                node.children.append(child)
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True, child, _vd + 1)[1]
            if child is not None:
                child.score = new_score
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                if node is not None and _vd < TREE_VIZ_DEPTH:
                    for pcol in valid_locations[i + 1:]:
                        node.children.append(TreeNode(col=pcol, maximizing=True, pruned=True))
                break
        return (best_col, value)


def pick_best_move(board, piece):
    root = TreeNode(col=None, maximizing=True)
    col, score = minimax(board, 5, float("-inf"), float("inf"), True, root)
    root.score = score
    return col, root

def print_board(board):
    print(np.flip(board, 0))
