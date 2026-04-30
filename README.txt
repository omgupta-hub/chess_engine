# ♟ Chess AI Engine

A fully playable chess engine built from scratch in Python, featuring a graphical interface and an AI opponent that plays at approximately **1600 ELO** — the level of a strong club player.

---

## 📸 Preview

> Play as White against a Black AI opponent on a fully interactive Pygame board. Valid moves are highlighted in blue, the AI's last move in purple, and check in red.

---

## 🧠 How the AI Works

The AI is powered by four layered techniques, each contributing to its strength:

### 1. Minimax Algorithm
The AI models the game as a decision tree. It searches **4 moves deep**, considering every possible position and choosing the move that guarantees the best outcome — assuming the opponent also plays optimally.

### 2. Alpha-Beta Pruning
A mathematical optimization that eliminates branches of the search tree that cannot possibly affect the final decision. Cuts 50–90% of positions that would otherwise be evaluated, allowing the engine to search deeper in the same time.

### 3. Piece-Square Tables (PST)
Each piece type has a 64-value positional bonus table. A knight in the center gets a bonus; a king exposed in the center during the middlegame gets a penalty. Separate tables are used for **middlegame** and **endgame** phases. This gives the AI genuine positional understanding.

### 4. Quiescence Search
Extends the search beyond depth 4 — but **only for captures** — until the position is "quiet" (no immediate exchanges). Fixes the horizon effect, where the engine might miss a capture just outside its search window.

### Additional Techniques
- **Move Ordering (MVV-LVA):** Captures are searched first, best captures first, making alpha-beta pruning far more effective.
- **Mobility Bonus:** The AI values having more available moves than the opponent (+5 centipawns per extra move).
- **Mop-Up Score:** In winning endgames, the AI is rewarded for pushing the enemy king toward corners and bringing its own king closer, enabling forced checkmate.
- **Stalemate Avoidance:** The engine explicitly detects and avoids moves that would stalemate the opponent when it is already winning.

---

## 🎮 Features

- ✅ Full legal move enforcement including all special rules
- ✅ **Castling** — both kingside and queenside, with all legality checks
- ✅ **En Passant** — correctly tracked and cleared after one turn
- ✅ **Pawn Promotion** — human chooses piece; AI always promotes to Queen
- ✅ **Check detection** — king highlighted in red when in check
- ✅ **Checkmate & Stalemate** detection with correct game-over handling
- ✅ **Threefold Repetition** draw detection
- ✅ **Move Undo** system powering the AI's full search tree
- ✅ Graphical board with highlighted valid moves, last AI move, and check indicator
- ✅ Playable as White vs Black AI

---

## 🗂 Project Structure

```
chess-ai/
│
├── Main.py           # Game loop, Pygame event handling, AI turn trigger
├── Board.py          # 8×8 board, move history, check/checkmate/draw logic
├── Piece.py          # All 6 piece classes with full movement rules
├── ChessEngine.py    # Minimax, Alpha-Beta, evaluation, quiescence search
│
└── Image/            # Piece images (PNG format)
    ├── white-King.png
    ├── white-Queen.png
    ├── white-Rook.png
    ├── white-Bishop.png
    ├── white-Knight.png
    ├── white-Pawn.png
    ├── black-King.png
    ├── black-Queen.png
    ├── black-Rook.png
    ├── black-Bishop.png
    ├── black-Knight.png
    └── black-Pawn.png
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Install dependencies

```bash
pip install pygame
```

### Run the game

```bash
python Main.py
```

You play as **White**. Click a piece to select it (valid moves highlighted in blue), then click a destination square to move. The AI (Black) responds automatically.

---

## 🕹 How to Play

| Action | How |
|---|---|
| Select a piece | Left-click on any of your white pieces |
| See valid moves | Blue dots appear on all legal destination squares |
| Move a piece | Click any highlighted (blue) square |
| Deselect | Click on an empty square or another of your pieces |
| Pawn promotion | Type `Q`, `R`, `B`, or `N` in the terminal when prompted |

### Board Colour Legend

| Colour | Meaning |
|---|---|
| 🔵 Dark Blue | Valid move destinations for selected piece |
| 🟣 Purple | Square where the AI just moved |
| 🔴 Red | King's square when it is in check |
| ⬜ White / 🔷 Blue-grey | Standard board squares |

---

## 📊 Evaluation Function

Positions are scored in **centipawns** from Black's perspective (positive = good for Black).

| Piece | Value (centipawns) |
|---|---|
| Pawn | 100 |
| Knight | 320 |
| Bishop | 330 |
| Rook | 500 |
| Queen | 900 |
| King | 20,000 |

Positional bonuses from piece-square tables are added on top of raw material values.

---

## 🔮 Roadmap / Future Improvements

- [ ] **Neural Network Evaluation** — replace hand-crafted eval with a net trained on grandmaster games (Stockfish NNUE approach)
- [ ] **Self-Play Reinforcement Learning** — AI improves by playing millions of games against itself (AlphaZero approach)
- [ ] **Opening Book** — preloaded database of strong opening lines for faster, stronger early game
- [ ] **Endgame Tablebase** — perfect play in all positions with 5 or fewer pieces
- [ ] **Bitboard Representation** — replace the 8×8 Python list with 64-bit integers for 10–20× faster move generation
- [ ] **In-game promotion UI** — replace terminal input with a graphical piece selector
- [ ] **Difficulty levels** — adjustable search depth for different player skill levels
- [ ] **PGN export** — save and replay games in standard chess notation

---

## 🧩 Architecture Overview

```
Main.py
  └── Creates Board, runs Pygame event loop
  └── Calls get_best_move() on the AI's turn

Board.py
  └── Holds the 8×8 grid (list of Piece objects / None)
  └── Tracks turn, history, en passant, check, draw conditions
  └── undo_move() enables the AI to simulate and reverse moves

Piece.py
  └── Base Piece class: move(), draw(), path_is_clear()
  └── Subclasses: Pawn, Rook, Bishop, Knight, Queen, King
  └── Each implements get_valid_moves()
  └── King implements can_castle() and castle()

ChessEngine.py
  └── evaluate_board()   — scores any position in centipawns
  └── minimax()          — recursive tree search with alpha-beta
  └── quiescence()       — extends search on captures only
  └── get_best_move()    — root call, returns (piece, move) tuple
```

---

## 📚 Concepts & References

- [Minimax Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- [Alpha-Beta Pruning — Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Piece-Square Tables — Chess Programming Wiki](https://www.chessprogramming.org/Piece-Square_Tables)
- [Quiescence Search — Chess Programming Wiki](https://www.chessprogramming.org/Quiescence_Search)
- [AlphaZero — DeepMind](https://deepmind.google/discover/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)

---

## 👤 Author

**[Your Name]**
[Your College / Institution]
[Your GitHub Profile Link]

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).