# test_load.py

from engine.analyzer import load_games_from_folder, extract_moves_from_game

games = load_games_from_folder("data/raw")

print(f"Found {len(games)} game(s).")

for i, game in enumerate(games[:3], 1):  # Preview up to 3 games
    moves = extract_moves_from_game(game)
    print(f"\nGame {i} moves:")
    print(" ".join(moves))
