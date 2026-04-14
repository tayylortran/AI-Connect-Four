# Runs a headless Connect Four game between two AIPlayer instances.
# Returns per-game stats and a list of per-move stats for logging.

import time
from src.connect4 import (
    create_board, drop_piece, get_next_open_row,
    winning_move, get_valid_locations, PLAYER_PIECE, AI_PIECE
)


def run_game(ai1, ai2):
    """
    ai1 plays as PLAYER_PIECE, ai2 plays as AI_PIECE.
    Returns (game_record dict, list of move_record dicts).
    """
    board = create_board()
    ais = [ai1, ai2]
    pieces = [PLAYER_PIECE, AI_PIECE]
    turn = 0
    move_num = 0
    move_records = []
    game_start = time.time()

    while True:
        current_ai = ais[turn]
        current_piece = pieces[turn]

        t0 = time.time()
        col = current_ai.get_move(board, current_piece)
        elapsed_ms = round((time.time() - t0) * 1000, 2)

        move_records.append({
            'move_num': move_num,
            'ai_name': current_ai.name,
            'col_chosen': col,
            'score': current_ai.last_score,
            'nodes_evaluated': current_ai.nodes_evaluated,
            'time_ms': elapsed_ms,
        })

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_piece)
        move_num += 1

        if winning_move(board, current_piece):
            winner = current_ai.name
            break
        if not get_valid_locations(board):
            winner = None  # draw
            break

        turn = 1 - turn

    game_record = {
        'ai1_name': ai1.name,
        'ai2_name': ai2.name,
        'winner': winner if winner is not None else 'Draw',
        'total_moves': move_num,
        'duration_seconds': round(time.time() - game_start, 3),
    }
    return game_record, move_records
