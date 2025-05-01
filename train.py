import os
import sys
import torch
import json
import pandas as pd
from tqdm import tqdm
from torch.utils.data import DataLoader
from torch import nn, optim

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from model.dataset import ChessDataset
from model.model import ChessNet

# Load dataset
dataset = ChessDataset("data/processed/your_moves_encoded.csv")
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Load move vocabulary size
with open("data/processed/move_vocab.json") as f:
    move_to_index = json.load(f)
num_classes = len(move_to_index)

# Initialize model
model = ChessNet(num_classes)
checkpoint_path = "data/processed/chess_model.pt"

# ✅ Resume from checkpoint if it exists
if os.path.exists(checkpoint_path):
    print("🔁 Loading model checkpoint...")
    model.load_state_dict(torch.load(checkpoint_path))
else:
    print("🆕 Starting new model training.")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Number of additional training epochs
epochs = 20

# 🔁 Training loop
for epoch in range(epochs):
    total_loss = 0
    progress = tqdm(loader, desc=f"Epoch {epoch+1}/{epochs}", leave=False)

    for X, y in progress:
        X, y = X.to(device), y.to(device)

        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        progress.set_postfix(loss=loss.item())

    print(f"✅ Epoch {epoch+1}/{epochs} — Total Loss: {total_loss:.4f}")

    # Save model after each epoch
    torch.save(model.state_dict(), checkpoint_path)

print("💾 Final model saved to:", checkpoint_path)
