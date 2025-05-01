# engine/analyzer.py

import chess.pgn
import os

def load_games_from_folder(folder_path):
    games = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pgn"):
            with open(os.path.join(folder_path, filename), encoding="utf-8") as pgn:
                while True:
                    game = chess.pgn.read_game(pgn)
                    if game is None:
                        break
                    games.append(game)
    return games

def extract_moves_from_game(game):
    board = game.board()
    moves = []
    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)
    return moves
