import argparse
import csv
from collections import defaultdict
from pathlib import Path


DATA_DIR = Path("data")


def newest_csv(prefix: str) -> Path:
    matches = sorted(DATA_DIR.glob(f"{prefix}_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        raise FileNotFoundError(f"No files matching {prefix}_*.csv were found in {DATA_DIR}.")
    return matches[0]


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def avg(rows, key):
    if not rows:
        return 0.0
    return sum(float(row[key]) for row in rows) / len(rows)


def matchup_key(row):
    left = (row["ai1_name"], row.get("ai1_depth", ""), row.get("ai1_heuristic", ""))
    right = (row["ai2_name"], row.get("ai2_depth", ""), row.get("ai2_heuristic", ""))
    return tuple(sorted((left, right)))


def matchup_label(key):
    (left_name, left_depth, left_heuristic), (right_name, right_depth, right_heuristic) = key
    return (
        f"{left_name} [depth={left_depth or 'n/a'}, heuristic={left_heuristic or 'n/a'}] vs "
        f"{right_name} [depth={right_depth or 'n/a'}, heuristic={right_heuristic or 'n/a'}]"
    )


def print_game_summary(game_rows):
    print("Game Summary")
    print(f"Total games: {len(game_rows)}")
    print(f"Average moves per game: {avg(game_rows, 'total_moves'):.2f}")
    print(f"Average duration per game: {avg(game_rows, 'duration_seconds'):.2f}s")
    print()

    grouped = defaultdict(list)
    for row in game_rows:
        grouped[matchup_key(row)].append(row)

    print("Matchups")
    for key, rows in grouped.items():
        wins = defaultdict(int)
        for row in rows:
            wins[row["winner"]] += 1

        print(matchup_label(key))
        print(
            f"  games={len(rows)}, avg_moves={avg(rows, 'total_moves'):.2f}, "
            f"avg_duration={avg(rows, 'duration_seconds'):.2f}s"
        )
        for winner, count in sorted(wins.items()):
            print(f"  {winner}: {count}")
        print()


def print_move_summary(move_rows):
    print("Move Summary")
    grouped = defaultdict(list)
    for row in move_rows:
        grouped[row["ai_name"]].append(row)

    for ai_name, rows in grouped.items():
        print(ai_name)
        print(
            f"  moves={len(rows)}, avg_time={avg(rows, 'time_ms'):.2f}ms, "
            f"avg_nodes={avg(rows, 'nodes_evaluated'):.2f}, avg_score={avg(rows, 'score'):.2f}"
        )
        print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze existing Connect Four simulation CSV results."
    )
    parser.add_argument(
        "games_csv",
        nargs="?",
        default=None,
        help="Path to a games CSV. Defaults to the newest data/games_*.csv file.",
    )
    parser.add_argument(
        "moves_csv",
        nargs="?",
        default=None,
        help="Path to a moves CSV. Defaults to the newest data/moves_*.csv file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    games_path = Path(args.games_csv) if args.games_csv else newest_csv("games")
    moves_path = Path(args.moves_csv) if args.moves_csv else newest_csv("moves")

    game_rows = read_csv(games_path)
    move_rows = read_csv(moves_path)

    print(f"Games CSV: {games_path}")
    print(f"Moves CSV: {moves_path}")
    print()
    print_game_summary(game_rows)
    print_move_summary(move_rows)


if __name__ == "__main__":
    main()
