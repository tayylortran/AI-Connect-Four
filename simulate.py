# Entry point for running AI vs AI simulations and logging results to CSV.
# Usage: python simulate.py
# Output: data/games_<timestamp>.csv and data/moves_<timestamp>.csv

from src.ai import RandomAI, GreedyAI, MinimaxAI
from src.ai.heuristics import aggressive_heuristic, balanced_heuristic, defensive_heuristic
from src.simulation import run_game
from src.logger import CSVLogger

# --- Configure matchups and number of games here ---
MATCHUPS = [
    (MinimaxAI(depth=5, heuristic=aggressive_heuristic),  MinimaxAI(depth=5, heuristic=defensive_heuristic)),
]
GAMES_PER_MATCHUP = 100
# ---------------------------------------------------

def main():
    total = len(MATCHUPS) * GAMES_PER_MATCHUP
    print(f"Running {total} games across {len(MATCHUPS)} matchups...\n")

    with CSVLogger() as logger:
        game_id = 0
        for ai1, ai2 in MATCHUPS:
            wins = {ai1.name: 0, ai2.name: 0, 'Draw': 0}
            for _ in range(GAMES_PER_MATCHUP):
                game, moves = run_game(ai1, ai2)
                logger.log(game_id, game, moves)
                wins[game['winner']] += 1
                game_id += 1

            print(f"{ai1.name} vs {ai2.name}")
            for name, count in wins.items():
                print(f"  {name}: {count}")
            print()

if __name__ == "__main__":
    main()
