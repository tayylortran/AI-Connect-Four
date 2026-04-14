# CSV logger for simulation data. Use as a context manager.
# Writes two files: games_<timestamp>.csv and moves_<timestamp>.csv

import csv
import os
from datetime import datetime


class CSVLogger:
    GAME_FIELDS = ['game_id', 'ai1_name', 'ai2_name', 'winner', 'total_moves', 'duration_seconds']
    MOVE_FIELDS = ['game_id', 'move_num', 'ai_name', 'col_chosen', 'score', 'nodes_evaluated', 'time_ms']

    def __init__(self, output_dir='data'):
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._game_path = os.path.join(output_dir, f'games_{ts}.csv')
        self._move_path = os.path.join(output_dir, f'moves_{ts}.csv')

    def __enter__(self):
        self._game_file = open(self._game_path, 'w', newline='')
        self._move_file = open(self._move_path, 'w', newline='')
        self._game_writer = csv.DictWriter(self._game_file, fieldnames=self.GAME_FIELDS)
        self._move_writer = csv.DictWriter(self._move_file, fieldnames=self.MOVE_FIELDS)
        self._game_writer.writeheader()
        self._move_writer.writeheader()
        return self

    def log(self, game_id, game_record, move_records):
        self._game_writer.writerow({'game_id': game_id, **game_record})
        for move in move_records:
            self._move_writer.writerow({'game_id': game_id, **move})
        # Flush after each game so data isn't lost if the run is interrupted
        self._game_file.flush()
        self._move_file.flush()

    def __exit__(self, *args):
        self._game_file.close()
        self._move_file.close()
        print(f"Saved: {self._game_path}")
        print(f"Saved: {self._move_path}")
