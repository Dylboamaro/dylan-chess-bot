# scripts/encode_moves.py

import pandas as pd
import chess
import json
from tqdm import tqdm
import sys
import os

# Allow relative imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.utils import build_move_vocab

# Load dataset
df = pd.read_csv("data/processed/your_moves_only.csv")

# Convert SAN → UCI with tqdm
def san_to_uci(fen, san_move):
    board = chess.Board(fen)
    move = board.parse_san(san_move)
    return move.uci()

tqdm.pandas(desc="Converting SAN to UCI")
df["uci_move"] = df.progress_apply(lambda row: san_to_uci(row["fen"], row["move"]), axis=1)

# Build move vocab
move_to_index, index_to_move = build_move_vocab(df["uci_move"])
df["move_idx"] = df["uci_move"].map(move_to_index)

# Save vocab
with open("data/processed/move_vocab.json", "w") as f:
    json.dump(move_to_index, f)

# Save updated dataset
df.to_csv("data/processed/your_moves_encoded.csv", index=False)

print("✅ Done: Moves encoded and saved.")
