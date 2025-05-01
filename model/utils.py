import numpy as np
import chess

# Piece-to-channel index
piece_to_index = {
    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
}

def fen_to_tensor(fen):
    board = chess.Board(fen)
    tensor = np.zeros((8, 8, 12), dtype=np.uint8)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            channel = piece_to_index[piece.symbol()]
            tensor[row, col, channel] = 1

    return tensor

def build_move_vocab(moves):
    """Given a list of moves (in UCI), return a move-to-index dictionary"""
    unique_moves = sorted(set(moves))
    move_to_index = {move: idx for idx, move in enumerate(unique_moves)}
    index_to_move = {idx: move for move, idx in move_to_index.items()}
    return move_to_index, index_to_move

