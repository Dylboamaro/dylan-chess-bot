import random
import pickle
import chess
import chess.engine
from collections import defaultdict

def build_position_move_map(games):
    position_move_map = defaultdict(list)

    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            fen = board.board_fen()
            position_move_map[fen].append(move)
            board.push(move)

    return position_move_map

def get_most_common_move(board, position_move_map):
    fen = board.board_fen()
    moves = position_move_map.get(fen)
    if not moves:
        return None
    return max(set(moves), key=moves.count)

def save_position_map(position_move_map, filepath="data/processed/position_map.pkl"):
    with open(filepath, "wb") as f:
        pickle.dump(position_move_map, f)

def load_position_map(filepath="data/processed/position_map.pkl"):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def determine_phase(move_number):
    if move_number <= 10:
        return "opening"
    elif move_number <= 30:
        return "middlegame"
    else:
        return "endgame"

def stockfish_fallback_move(board, engine_path=r"C:\\Users\\user\\repos\\chess-playstyle-engine\\engine\\stockfish\\stockfish.exe"):
    phase_profiles = {
        "opening": {
            "best": 0.12,
            "inaccuracy": 0.60,
            "mistake": 0.23,
            "blunder": 0.05,
        },
        "middlegame": {
            "best": 0.08,
            "inaccuracy": 0.30,
            "mistake": 0.32,
            "blunder": 0.30,
        },
        "endgame": {
            "best": 0.06,
            "inaccuracy": 0.14,
            "mistake": 0.26,
            "blunder": 0.54,
        },
    }

    try:
        with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
            info = engine.analyse(board, chess.engine.Limit(time=0.3))
            best_score = info["score"].relative.score(mate_score=10000) or 0

            move_buckets = {"best": [], "inaccuracy": [], "mistake": [], "blunder": []}

            for move in board.legal_moves:
                board.push(move)
                try:
                    analysis = engine.analyse(board, chess.engine.Limit(time=0.2))
                    score = analysis["score"].relative.score(mate_score=10000) or 0
                except Exception:
                    score = best_score
                board.pop()

                cp_loss = abs(best_score - score)

                if cp_loss < 20:
                    move_buckets["best"].append(move)
                elif cp_loss < 100:
                    move_buckets["inaccuracy"].append(move)
                elif cp_loss < 300:
                    move_buckets["mistake"].append(move)
                else:
                    move_buckets["blunder"].append(move)

            move_number = board.fullmove_number * 2 - (0 if board.turn == chess.WHITE else 1)
            phase = determine_phase(move_number)
            profile = phase_profiles[phase]

            categories = list(profile.keys())
            weights = list(profile.values())
            chosen_category = random.choices(categories, weights=weights, k=1)[0]

            for fallback in [chosen_category, "mistake", "inaccuracy", "best", "blunder"]:
                if move_buckets[fallback]:
                    return random.choice(move_buckets[fallback])

            return random.choice(list(board.legal_moves))

    except Exception as e:
        print(f"Stockfish fallback failed: {e}")
        return random.choice(list(board.legal_moves))