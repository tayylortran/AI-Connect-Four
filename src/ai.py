from src.connect4 import (
    get_valid_locations, is_terminal_node, winning_move,
    get_next_open_row, copy_board, drop_piece, score_position,
    AI_PIECE, PLAYER_PIECE
)

def minimax(board, depth, alpha, beta, maximizing_player):
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
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
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
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (best_col, value)


def pick_best_move(board, piece):
    col, _ = minimax(board, 5, float("-inf"), float("inf"), True)
    return col
