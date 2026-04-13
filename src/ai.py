from src.connect4 import (
    get_valid_locations, is_terminal_node, winning_move,
    get_next_open_row, copy_board, drop_piece, score_position,
    AI_PIECE, PLAYER_PIECE
)

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
