# Tic-Tac-Toe — Human vs Computer

A command-line Tic-Tac-Toe game (3 × 3 board) with two computer strategies.

---

## Problem Statement

| Item | Description |
|---|---|
| **Players** | Human (`X`) vs Computer (`O`) |
| **Board** | 3 × 3 grid, cells numbered 1 – 9 |
| **Turn order** | Human always moves first; turns alternate |
| **Win condition** | Fill any full row, column, or diagonal with your mark |
| **Draw condition** | All 9 cells occupied with no winner |
| **Input** | Integer 1 – 9 per turn |
| **Output** | Updated board after each move; result message at game end |

---

## Algorithm / Strategy

### Random Move Strategy
```
1. Collect all empty cells.
2. Pick one at random.
3. Place the computer's mark there.
```

### Intelligent Move Strategy
```
Priority 1 – WIN  : Is there a cell that completes the computer's line?
              → Take it immediately.

Priority 2 – BLOCK: Is there a cell that completes the human's line?
              → Take it to prevent the human from winning.

Priority 3 – CENTRE: Is cell 5 (index 4) free?
              → Take the centre (strongest positional choice).

Priority 4 – OPPOSITE CORNER: Does the human hold a corner?
              → Take the diagonally opposite corner.

Priority 5 – ANY CORNER: Take a random free corner.
              (Corners provide more winning lines than edges.)

Priority 6 – ANY EDGE: Take a random free edge cell.

Tie-break within any priority tier is resolved randomly.
```

---

## File Structure

```
tictactoe.py   – single self-contained module
README.md      – this file
```

---

## Requirements

- Python 3.7+  (standard library only — no third-party packages needed)

---

## How to Run

```bash
python tictactoe.py
```

1. Choose a strategy: **1** (Random) or **2** (Intelligent).
2. Enter a cell number **1 – 9** when it is your turn.
3. The board updates after every move.
4. The game announces **You Win / Computer Wins / Draw** at the end.
5. Optionally play again; a running session score is displayed.

---

## Board Cell Numbering

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

---

## Input Validation

| Check | Error message |
|---|---|
| Non-digit input | `⚠  Invalid input. Please enter a single digit (1-9).` |
| Number outside 1-9 | `⚠  Number out of range. Enter 1 through 9.` |
| Already occupied cell | `⚠  That cell is already occupied. Choose another.` |

---

## Sample Session

```
╔══════════════════════════════════════════════╗
║       TIC-TAC-TOE  –  Human  vs  Computer   ║
╚══════════════════════════════════════════════╝

  Select computer strategy:
    1 – Random Move
    2 – Intelligent Move
  Enter 1 or 2: 2

══════════════════════════════════════════════════
  Tic-Tac-Toe  │  Strategy: Intelligent Move Strategy
══════════════════════════════════════════════════
  You are X.  Computer is O.

 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9

── YOUR TURN ───────────────────────────────
Your move — enter a cell number (1-9): 1

 X | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9

── COMPUTER'S TURN ─────────────────────────
  Computer chose cell 5.

 X | 2 | 3
---+---+---
 4 | O | 6
---+---+---
 7 | 8 | 9
...
```

---

## License

MIT
