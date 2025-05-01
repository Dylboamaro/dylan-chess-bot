import os
import chess.pgn
import chess.engine
from engine.analyzer import load_games_from_folder
from tqdm import tqdm

# ✅ Update this path to your actual Stockfish executable
STOCKFISH_PATH = r"C:\Users\user\repos\chess-playstyle-engine\engine\stockfish\stockfish.exe"

def determine_phase(move_number):
    if move_number <= 10:
        return "opening"
    elif move_number <= 30:
        return "middlegame"
    else:
        return "endgame"

def classify_move_score(diff_cp):
    """
    Classify move quality based on centipawn difference between
    best move and played move.
    """
    if diff_cp < 20:
        return "best"
    elif diff_cp < 100:
        return "inaccuracy"
    elif diff_cp < 300:
        return "mistake"
    else:
        return "blunder"

def analyze_games(games, max_games=None):
    """
    Analyze PGN games, evaluate move quality, and return stats split by phase.
    """
    stats = {
        "opening": {"best": 0, "inaccuracy": 0, "mistake": 0, "blunder": 0, "total": 0},
        "middlegame": {"best": 0, "inaccuracy": 0, "mistake": 0, "blunder": 0, "total": 0},
        "endgame": {"best": 0, "inaccuracy": 0, "mistake": 0, "blunder": 0, "total": 0},
    }

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        for game in tqdm(games[:max_games]):
            board = game.board()

            for move in game.mainline_moves():
                move_number = board.fullmove_number * 2 - (0 if board.turn == chess.WHITE else 1)
                phase = determine_phase(move_number)

                try:
                    # Evaluate best move before user's move
                    info = engine.analyse(board, chess.engine.Limit(depth=8))
                    pv = info.get("pv")
                    if not pv:
                        continue
                    best_move = pv[0]
                    best_score = info["score"].relative.score(mate_score=10000) or 0

                    board.push(move)

                    # Evaluate the played move
                    info_after = engine.analyse(board, chess.engine.Limit(depth=8))
                    after_score = info_after["score"].relative.score(mate_score=10000) or 0

                    cp_loss = abs(best_score - after_score)
                    category = classify_move_score(cp_loss)

                    stats[phase][category] += 1
                    stats[phase]["total"] += 1

                except Exception as e:
                    board.pop()
                    continue

    return stats
