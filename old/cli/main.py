import random
import chess
from engine.simulator import (
    load_position_map,
    get_most_common_move,
    stockfish_fallback_move,
)

def play_against_self(position_map_path="data/processed/position_map.pkl"):
    print("Loading engine...")
    position_move_map = load_position_map(position_map_path)

    board = chess.Board()
    print(board)

    while not board.is_game_over():
        # --- Human move ---
        while True:
            user_input = input("\nYour move (e.g. e4, Nf3, O-O): ").strip()
            try:
                move = board.parse_san(user_input)
                if move in board.legal_moves:
                    board.push(move)
                    break
                else:
                    print("Illegal move. Try again.")
            except:
                print("Invalid move format or illegal move. Try again.")

        print("\nBoard after your move:")
        print(board)

        if board.is_game_over():
            break

        # --- Simulated you (fallback with Stockfish) ---
        print("\nYour simulated self is thinking...")
        response_move = get_most_common_move(board, position_move_map)

        if response_move is None:
            print("No historical data — choosing move via Stockfish fallback.")
            response_move = stockfish_fallback_move(board)

        san_move = board.san(response_move)
        board.push(response_move)
        print(f"\nSimulated you plays: {san_move}")
        print(board)

    print("\nGame Over:", board.result())
    outcome = board.outcome()
    if outcome:
        print(outcome.termination.name)
    else:
        print("Game not actually over — loop exited unexpectedly.")

if __name__ == "__main__":
    play_against_self()
