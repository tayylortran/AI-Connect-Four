# Runs a headless Connect Four game between two AIPlayer instances.
# Returns per-game stats and a list of per-move stats for logging.

import time
from src.connect4 import (
    create_board, drop_piece, get_next_open_row,
    winning_move, get_valid_locations, PLAYER_PIECE, AI_PIECE
)


def _ai_metadata(ai):
    heuristic = getattr(ai, "heuristic", None)
    return {
        'ai_type': ai.__class__.__name__,
        'depth': getattr(ai, "depth", ""),
        'heuristic': heuristic.__name__ if heuristic is not None else "",
    }


def run_game(ai1, ai2):
    """
    ai1 plays as PLAYER_PIECE, ai2 plays as AI_PIECE.
    Returns (game_record dict, list of move_record dicts).
    """
    board = create_board()
    ais = [ai1, ai2]
    pieces = [PLAYER_PIECE, AI_PIECE]
    ai1_meta = _ai_metadata(ai1)
    ai2_meta = _ai_metadata(ai2)
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
            'ai_type': current_ai.__class__.__name__,
            'ai_depth': getattr(current_ai, "depth", ""),
            'ai_heuristic': getattr(getattr(current_ai, "heuristic", None), "__name__", ""),
            'piece': current_piece,
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
        'ai1_type': ai1_meta['ai_type'],
        'ai1_depth': ai1_meta['depth'],
        'ai1_heuristic': ai1_meta['heuristic'],
        'ai2_name': ai2.name,
        'ai2_type': ai2_meta['ai_type'],
        'ai2_depth': ai2_meta['depth'],
        'ai2_heuristic': ai2_meta['heuristic'],
        'starting_ai': ai1.name,
        'winner': winner if winner is not None else 'Draw',
        'is_draw': winner is None,
        'total_moves': move_num,
        'duration_seconds': round(time.time() - game_start, 3),
    }
    return game_record, move_records
