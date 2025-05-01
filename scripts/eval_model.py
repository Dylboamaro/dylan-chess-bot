import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
from model.utils import fen_to_tensor
from model.model import ChessNet

# Load data
df = pd.read_csv("data/processed/your_moves_encoded.csv")

# Split off 10% as test set
test_df = df.sample(frac=0.10, random_state=42).reset_index(drop=True)

# Load vocab
with open("data/processed/move_vocab.json") as f:
    move_to_index = json.load(f)
index_to_move = {v: k for k, v in move_to_index.items()}

# Load model
num_classes = len(move_to_index)
model = ChessNet(num_classes)
model.load_state_dict(torch.load("data/processed/chess_model.pt", map_location="cpu"))
model.eval()

# Evaluate top-1 accuracy
correct = 0
total = len(test_df)

print(f"📊 Evaluating top-1 accuracy on {total} test positions...\n")

for _, row in tqdm(test_df.iterrows(), total=total, desc="Checking moves"):
    fen = row["fen"]
    true_idx = row["move_idx"]

    board_tensor = fen_to_tensor(fen)
    board_tensor = np.transpose(board_tensor, (2, 0, 1))  # (12, 8, 8)
    input_tensor = torch.from_numpy(board_tensor).unsqueeze(0).float()

    with torch.no_grad():
        output = model(input_tensor)
        predicted_idx = torch.argmax(output, dim=1).item()

    if predicted_idx == true_idx:
        correct += 1

accuracy = correct / total
print(f"\n✅ Final Top-1 Accuracy: {accuracy:.4%} ({correct}/{total})")
