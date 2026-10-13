"""
Tic-Tac-Toe Game
================
Problem Statement:
  Two players (Human vs Computer) play on a 3×3 board.
  - Human plays as 'X', Computer plays as 'O'.
  - Players alternate turns; Human always goes first.
  - A player wins by filling an entire row, column, or diagonal.
  - The game is a draw if all 9 cells are filled with no winner.

Inputs  : Cell number (1-9) chosen by the human each turn.
Outputs : Board state after each move; final result (Win / Loss / Draw).

Two computer strategies are provided:
  1. Random      – Computer picks any empty cell at random.
  2. Intelligent – Priority order:
       a) Win  : Take a winning move if available.
       b) Block: Block the human's immediate win.
       c) Centre → Opposite corner → Any corner → Any edge.
"""

import random
import sys


# ── Board helpers ─────────────────────────────────────────────────────────────

def make_board():
    """Return a fresh 9-element list (indices 0-8)."""
    return [" "] * 9


def display_board(board):
    """Pretty-print the 3×3 board; empty cells show their number (1-9)."""
    def cell(i):
        return board[i] if board[i] != " " else str(i + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()


# All eight possible winning combinations (row / col / diagonal)
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),               # diagonals
]


def check_winner(board, mark):
    """Return True if *mark* has completed any winning line."""
    return any(
        board[a] == board[b] == board[c] == mark
        for a, b, c in WIN_LINES
    )


def available_moves(board):
    """Return a list of indices that are still empty."""
    return [i for i, v in enumerate(board) if v == " "]


def is_draw(board):
    """True when the board is full with no winner."""
    return not available_moves(board)


# ── Computer strategies ───────────────────────────────────────────────────────

def computer_random(board, _computer_mark, _human_mark):
    """
    Random Move Strategy
    --------------------
    Picks a random empty cell with no strategic consideration.
    """
    return random.choice(available_moves(board))


def _find_winning_move(board, mark):
    """
    Scan every empty cell; return the first index that gives *mark*
    an immediate win, or None if no such cell exists.
    """
    for i in available_moves(board):
        board[i] = mark
        won = check_winner(board, mark)
        board[i] = " "          # undo
        if won:
            return i
    return None


def computer_intelligent(board, computer_mark, human_mark):
    """
    Intelligent Move Strategy
    -------------------------
    Evaluates moves in strict priority order:
      1. Win        – take the cell that completes the computer's own line.
      2. Block       – stop the human from winning on their next turn.
      3. Centre      – cell 4 (index 4) is the strongest positional choice.
      4. Opp. corner – if the human occupies a corner, take the opposite one.
      5. Any corner  – corners offer more winning-line coverage than edges.
      6. Any edge    – last resort.
    Ties within a tier are broken randomly.
    """
    moves = available_moves(board)

    # Priority 1 – win immediately
    move = _find_winning_move(board, computer_mark)
    if move is not None:
        return move

    # Priority 2 – block human's immediate win
    move = _find_winning_move(board, human_mark)
    if move is not None:
        return move

    # Priority 3 – centre
    if 4 in moves:
        return 4

    # Priority 4 – opposite corner (counter-strategy)
    corners = [0, 2, 6, 8]
    opposite = {0: 8, 8: 0, 2: 6, 6: 2}
    opp = [opposite[c] for c in corners
           if board[c] == human_mark and opposite[c] in moves]
    if opp:
        return random.choice(opp)

    # Priority 5 – any free corner
    free_corners = [c for c in corners if c in moves]
    if free_corners:
        return random.choice(free_corners)

    # Priority 6 – any free edge
    edges = [1, 3, 5, 7]
    free_edges = [e for e in edges if e in moves]
    if free_edges:
        return random.choice(free_edges)

    return random.choice(moves)   # fallback (board almost full)


# ── Human input ───────────────────────────────────────────────────────────────

def human_move(board):
    """
    Prompt the human for a cell number (1-9), validate the input, and
    return the corresponding 0-based board index.
    Validation checks:
      • Must be a digit.
      • Must be in range 1-9.
      • Cell must not already be occupied.
    """
    while True:
        try:
            raw = input("Your move — enter a cell number (1-9): ").strip()
            idx = int(raw) - 1
            if not (0 <= idx <= 8):
                print("  ⚠  Number out of range. Enter 1 through 9.")
                continue
            if board[idx] != " ":
                print("  ⚠  That cell is already occupied. Choose another.")
                continue
            return idx
        except ValueError:
            print("  ⚠  Invalid input. Please enter a single digit (1-9).")


# ── Game loop ─────────────────────────────────────────────────────────────────

def play_game(strategy_fn, strategy_name):
    """
    Run one complete game of Tic-Tac-Toe.

    Parameters
    ----------
    strategy_fn   : callable(board, computer_mark, human_mark) -> int
    strategy_name : str   – displayed in the game header

    Returns
    -------
    "human" | "computer" | "draw"
    """
    board         = make_board()
    human_mark    = "X"
    computer_mark = "O"

    print(f"\n{'=' * 46}")
    print(f"  Tic-Tac-Toe  │  Strategy: {strategy_name}")
    print(f"{'=' * 46}")
    print("  You are X.  Computer is O.")
    print("  Cell layout:")
    display_board(board)          # shows numbers before any moves

    for turn in range(9):
        if turn % 2 == 0:         # even turns → Human (X goes first)
            print("── YOUR TURN ───────────────────────────────")
            idx = human_move(board)
            board[idx] = human_mark
        else:                      # odd turns → Computer
            print("── COMPUTER'S TURN ─────────────────────────")
            idx = strategy_fn(board, computer_mark, human_mark)
            board[idx] = computer_mark
            print(f"  Computer chose cell {idx + 1}.")

        display_board(board)

        if check_winner(board, human_mark):
            print("🎉  YOU WIN! Congratulations!\n")
            return "human"
        if check_winner(board, computer_mark):
            print("🤖  COMPUTER WINS! Better luck next time.\n")
            return "computer"

    # All 9 cells filled, no winner
    print("🤝  It's a DRAW!\n")
    return "draw"


# ── Menu ─────────────────────────────────────────────────────────────────────

STRATEGIES = {
    "1": ("Random Move Strategy",      computer_random),
    "2": ("Intelligent Move Strategy", computer_intelligent),
}


def select_strategy():
    """Ask the user to pick a strategy; validate and return (name, fn)."""
    print("\n  Select computer strategy:")
    print("    1 – Random Move")
    print("    2 – Intelligent Move")
    while True:
        choice = input("  Enter 1 or 2: ").strip()
        if choice in STRATEGIES:
            return STRATEGIES[choice]
        print("  ⚠  Please enter 1 or 2.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════════════╗")
    print("║       TIC-TAC-TOE  –  Human  vs  Computer   ║")
    print("╚══════════════════════════════════════════════╝")

    wins = losses = draws = 0

    while True:
        name, fn = select_strategy()
        result   = play_game(fn, name)

        if result == "human":
            wins += 1
        elif result == "computer":
            losses += 1
        else:
            draws += 1

        print(f"  ── Session Score ──────────────────────────")
        print(f"     Wins: {wins}   Losses: {losses}   Draws: {draws}")
        print(f"  ───────────────────────────────────────────")

        again = input("\n  Play again? (y / n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Goodbye. 👋\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
