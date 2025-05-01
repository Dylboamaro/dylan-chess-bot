# test_simulator.py

import os
from engine.analyzer import load_games_from_folder
from engine.simulator import (
    build_position_move_map,
    get_most_common_move,
    save_position_map,
    load_position_map,
)
import chess

MAP_PATH = "data/processed/position_map.pkl"

# Load from cache or build fresh
if os.path.exists(MAP_PATH):
    print("Loading cached position map...")
    position_move_map = load_position_map(MAP_PATH)
else:
    print("Building position map...")
    games = load_games_from_folder("data/raw")
    position_move_map = build_position_move_map(games)
    save_position_map(position_move_map, MAP_PATH)

# Test a position
fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 3"
board = chess.Board(fen=fen)

move = get_most_common_move(board, position_move_map)

if move:
    print(f"From this position, your most common move was: {board.san(move)}")
else:
    print("No match found for this position.")
