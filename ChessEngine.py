from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn

#  PIECE VALUES
PIECE_VALUES = {
    Pawn:   100,
    Knight: 320,
    Bishop: 330,
    Rook:   500,
    Queen:  900,
    King:   20000,
}

#  PIECE-SQUARE TABLES

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

PAWN_ENDGAME_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
     5,  5,  5,  5,  5,  5,  5,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_MIDDLEGAME_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]

KING_ENDGAME_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50,
]

PST_MIDDLEGAME = {
    Pawn: PAWN_TABLE, Knight: KNIGHT_TABLE, Bishop: BISHOP_TABLE,
    Rook: ROOK_TABLE, Queen: QUEEN_TABLE,   King: KING_MIDDLEGAME_TABLE,
}

PST_ENDGAME = {
    Pawn: PAWN_ENDGAME_TABLE, Knight: KNIGHT_TABLE, Bishop: BISHOP_TABLE,
    Rook: ROOK_TABLE,         Queen: QUEEN_TABLE,   King: KING_ENDGAME_TABLE,
}


#  HELPERS
def _get_material(board, color):
    total = 0
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == color and not isinstance(piece, (King, Pawn)):
                total += PIECE_VALUES.get(type(piece), 0)
    return total


def _is_endgame(board):
    return _get_material(board, 'white') <= 1300 and _get_material(board, 'black') <= 1300


def _pst_score(piece_type, row, col, is_white, endgame):
    table = (PST_ENDGAME if endgame else PST_MIDDLEGAME)[piece_type]
    index = row * 8 + col if is_white else (7 - row) * 8 + col
    return table[index]


def _mop_up_score(board, our_color, enemy_color):
    """Push enemy king to corner; bring our king close."""
    enemy_king_pos = None
    our_king_pos   = None
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if isinstance(piece, King):
                if piece.color == enemy_color:
                    enemy_king_pos = (row, col)
                else:
                    our_king_pos = (row, col)
    if not enemy_king_pos or not our_king_pos:
        return 0
    er, ec  = enemy_king_pos
    or_, oc = our_king_pos
    enemy_center_dist = abs(er - 3.5) + abs(ec - 3.5)
    king_distance     = max(abs(er - or_), abs(ec - oc))
    return int(10 * enemy_center_dist) + int(10 * (7 - king_distance))


# ──────────────────────────────────────────────────────────────
#  STALEMATE DETECTION  ← THE KEY FIX
# ──────────────────────────────────────────────────────────────

def _is_stalemate(board, color):
    """
    Returns True if `color` has no legal moves AND is NOT in check.
    A stalemate is a draw (score = 0), never a win.
    """
    try:
        if board.is_in_check(color):
            return False  # in check → would be checkmate, not stalemate

        moves = board.get_all_player_moves(color)
        for piece, move in moves:
            piece.move(move, board, True)
            still_in_check = board.is_in_check(color)
            board.undo_move()
            if not still_in_check:
                return False  # found at least one legal move → not stalemate
        return True           # no legal move and not in check → stalemate
    except Exception:
        return False


# ──────────────────────────────────────────────────────────────
#  EVALUATE BOARD
# ──────────────────────────────────────────────────────────────

def evaluate_board(board):
    """Score in centipawns from Black's perspective (positive = good for black)."""
    endgame = _is_endgame(board)
    score   = 0

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is None:
                continue
            piece_type = type(piece)
            value = PIECE_VALUES.get(piece_type, 0)
            pst   = _pst_score(piece_type, row, col, piece.color == 'white', endgame)
            if piece.color == 'white':
                score -= (value + pst)
            else:
                score += (value + pst)

    # Mobility bonus
    try:
        score += (len(board.get_all_player_moves('black')) -
                  len(board.get_all_player_moves('white'))) * 5
    except Exception:
        pass

    # Mop-up: drive enemy king to corner when winning in endgame
    if endgame and score > 200:
        score += _mop_up_score(board, 'black', 'white')
    elif endgame and score < -200:
        score -= _mop_up_score(board, 'white', 'black')

    return score


# ──────────────────────────────────────────────────────────────
#  MOVE ORDERING
# ──────────────────────────────────────────────────────────────

def _move_score(board, piece, move):
    target = board.get_piece(move[0], move[1])
    if target is not None:
        return PIECE_VALUES.get(type(target), 0) - PIECE_VALUES.get(type(piece), 0) // 10
    return 0


def _order_moves(board, moves):
    return sorted(moves, key=lambda pm: _move_score(board, pm[0], pm[1]), reverse=True)


# ──────────────────────────────────────────────────────────────
#  QUIESCENCE SEARCH
# ──────────────────────────────────────────────────────────────

def quiescence(board, alpha, beta, maximizing_player, depth=0):
    stand_pat = evaluate_board(board)
    if maximizing_player:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)
    if depth >= 4:
        return stand_pat
    try:
        color     = board.get_current_player_color()
        all_moves = board.get_all_player_moves(color)
    except Exception:
        return stand_pat
    captures = _order_moves(board, [
        (p, m) for p, m in all_moves if board.get_piece(m[0], m[1]) is not None
    ])
    if not captures:
        return stand_pat
    for piece, move in captures:
        piece.move(move, board, True)
        score = quiescence(board, alpha, beta, not maximizing_player, depth + 1)
        board.undo_move()
        if maximizing_player:
            alpha = max(alpha, score)
            if alpha >= beta:
                return beta
        else:
            beta = min(beta, score)
            if beta <= alpha:
                return alpha
    return alpha if maximizing_player else beta


# ──────────────────────────────────────────────────────────────
#  MINIMAX WITH ALPHA-BETA  — stalemate-aware
# ──────────────────────────────────────────────────────────────

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return quiescence(board, alpha, beta, maximizing_player)

    try:
        color = board.get_current_player_color()
        moves = board.get_all_player_moves(color)
    except Exception:
        return evaluate_board(board)

    moves = _order_moves(board, moves)

    # ── No moves: checkmate vs stalemate ─────────────────────────────────
    if not moves:
        try:
            in_check = board.is_in_check(color)
        except Exception:
            in_check = False

        if in_check:
            # Checkmate: the side to move has lost
            # If maximizing (black's turn) and black is mated → terrible for black
            return -99999 if maximizing_player else 99999
        else:
            # Stalemate: always a draw
            return 0

    if maximizing_player:
        max_eval = float('-inf')
        for piece, move in moves:
            piece.move(move, board, True)
            eval_ = minimax(board, depth - 1, alpha, beta, False)
            board.undo_move()
            max_eval = max(max_eval, eval_)
            alpha    = max(alpha, eval_)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for piece, move in moves:
            piece.move(move, board, True)
            eval_ = minimax(board, depth - 1, alpha, beta, True)
            board.undo_move()
            min_eval = min(min_eval, eval_)
            beta     = min(beta, eval_)
            if beta <= alpha:
                break
        return min_eval


# ──────────────────────────────────────────────────────────────
#  GET BEST MOVE — stalemate-avoiding at the root
# ──────────────────────────────────────────────────────────────

SEARCH_DEPTH = 4


def get_best_move(board, depth=SEARCH_DEPTH):
    best_score     = float('-inf')
    best_move      = None
    stalemate_move = None   # used only if every single move causes stalemate
    original_turn  = board.turn

    try:
        current_color = board.get_current_player_color()
        valid_moves   = board.get_all_player_moves(current_color)
    except Exception:
        return None

    if not valid_moves:
        return None

    opponent_color = 'white' if current_color == 'black' else 'black'
    valid_moves    = _order_moves(board, valid_moves)

    for piece, move in valid_moves:
        piece.move(move, board, True)

        # Skip moves that leave OWN king in check
        try:
            own_in_check = board.is_in_check(current_color)
        except Exception:
            own_in_check = False

        if own_in_check:
            board.undo_move()
            continue

        # ── STALEMATE GUARD ──────────────────────────────────────────────
        # If this move leaves the opponent with no legal moves but not in
        # check, it's a stalemate → draw. Skip it if we have better options.
        try:
            would_stalemate = _is_stalemate(board, opponent_color)
        except Exception:
            would_stalemate = False

        if would_stalemate:
            # Save as emergency fallback; don't evaluate further
            if stalemate_move is None:
                stalemate_move = (piece, move)
            board.undo_move()
            continue

        score = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.undo_move()

        if score > best_score:
            best_score = score
            best_move  = (piece, move)

    board.turn = original_turn

    # Edge case: every legal move stalemated the opponent.
    # Play the stalemate move rather than returning None (which would crash).
    if best_move is None:
        best_move = stalemate_move

    return best_move


# ──────────────────────────────────────────────────────────────
#  LEGACY STUBS
# ──────────────────────────────────────────────────────────────

def q_learning_update(*args, **kwargs):
    pass

def plot_learning_curve(*args, **kwargs):
    pass

losses = []