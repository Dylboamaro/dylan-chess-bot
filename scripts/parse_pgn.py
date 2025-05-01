import chess.pgn
import pandas as pd
from tqdm import tqdm

# Your usernames
usernames = {"dylboamaro", "DylboAmaro"}

pgn_path = "data/raw/all-games.pgn"
positions = []
moves = []

# Estimate total number of games
with open(pgn_path, "r", encoding="utf-8") as f:
    game_count = sum(1 for line in f if line.strip() == "")

with open(pgn_path, "r", encoding="utf-8") as pgn_file:
    for _ in tqdm(range(game_count), desc="Filtering your moves"):
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break

        white = game.headers.get("White", "")
        black = game.headers.get("Black", "")

        if white in usernames:
            your_color = chess.WHITE
        elif black in usernames:
            your_color = chess.BLACK
        else:
            continue  # Skip games not played by you

        board = game.board()
        for move in game.mainline_moves():
            if board.turn == your_color:
                positions.append(board.fen())
                moves.append(board.san(move))
            board.push(move)

# Save output
df = pd.DataFrame({
    "fen": positions,
    "move": moves
})
df.to_csv("data/processed/your_moves_only.csv", index=False)
