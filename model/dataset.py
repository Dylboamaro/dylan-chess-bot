# model/dataset.py

import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
from model.utils import fen_to_tensor

class ChessDataset(Dataset):
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        fen = self.df.iloc[idx]["fen"]
        move_idx = self.df.iloc[idx]["move_idx"]
        
        board_tensor = fen_to_tensor(fen)           # Shape: (8, 8, 12)
        board_tensor = np.transpose(board_tensor, (2, 0, 1))  # Now (12, 8, 8) for PyTorch
        
        return torch.tensor(board_tensor, dtype=torch.float32), torch.tensor(move_idx, dtype=torch.long)
