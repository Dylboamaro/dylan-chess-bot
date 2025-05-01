import chess
import chess.engine

board = chess.Board()
engine_path = r"C:\Users\user\repos\chess-playstyle-engine\engine\stockfish\stockfish.exe"

try:
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        result = engine.analyse(board, chess.engine.Limit(time=0.1))
        print("Stockfish is working! Best move:", result["pv"][0])
except Exception as e:
    print("Failed to launch Stockfish:", e)
