"""
Sudoku solver using backtracking with incremental state tracking.

LeetCode 37. Sudoku Solver (Hard)
https://leetcode.com/problems/sudoku-solver/
"""

from typing import List


Board = List[List[str]]


class SudokuSolver:
    """
    Solves a 9x9 Sudoku puzzle in-place using backtracking.

    The solver maintains three sets of seen digits (per row, column, and 3x3 box)
    that are updated incrementally as values are placed and removed during
    the search. This reduces validity checks to O(1) per candidate.

    Empty cells are represented by the character '.'.
    Filled cells contain digit characters '1'..'9'.

    Example:
        >>> board = [
        ...     ["5","3",".",".","7",".",".",".","."],
        ...     ["6",".",".","1","9","5",".",".","."],
        ...     # ...
        ... ]
        >>> solver = SudokuSolver(board)
        >>> solver.solve()
        True
        >>> solver.is_solved()
        True
    """

    BOARD_SIZE = 9
    BOX_SIZE = 3
    EMPTY = "."
    DIGITS = "123456789"

    def __init__(self, board: Board) -> None:
        """Initialize solver with a 9x9 board """
        if not self._has_valid_shape(board):
            raise ValueError("Board must be a 9x9 grid.")
        self.board = board
        self._rows: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        self._cols: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        self._boxes: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        self._initialize_state()

    # ---------- Public API ----------

    def solve(self) -> bool:
        """
        Solve the puzzle in place.

        Returns:
            True if a solution was found and the board is now filled,
            False if no solution exists.
        """
        return self._backtrack(0, 0)

    def is_solved(self) -> bool:
        """Return True if the board is fully filled and valid."""
        for row in self.board:
            if self.EMPTY in row:
                return False
        return self._is_currently_valid()

    def is_valid_board(self) -> bool:
        """Return True if the current board has no conflicts (may still be incomplete)."""
        return self._is_currently_valid()

    def count_empty(self) -> int:
        """Return the number of empty cells remaining."""
        return sum(row.count(self.EMPTY) for row in self.board)

    # ---------- Display ----------

    def __str__(self) -> str:
        """Return a human-readable representation of the board."""
        lines = []
        for r in range(self.BOARD_SIZE):
            if r > 0 and r % self.BOX_SIZE == 0:
                lines.append("-" * 21)
            row_cells = []
            for c in range(self.BOARD_SIZE):
                if c > 0 and c % self.BOX_SIZE == 0:
                    row_cells.append("|")
                row_cells.append(self.board[r][c])
            lines.append(" ".join(row_cells))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"SudokuSolver(empty_cells={self.count_empty()})"

    # ---------- Internal ----------

    def _backtrack(self, row: int, col: int) -> bool:
        if row == self.BOARD_SIZE:
            return True
        if col == self.BOARD_SIZE:
            return self._backtrack(row + 1, 0)
        if self.board[row][col] != self.EMPTY:
            return self._backtrack(row, col + 1)

        box = self._box_index(row, col)
        for digit in self.DIGITS:
            if (
                digit not in self._rows[row]
                and digit not in self._cols[col]
                and digit not in self._boxes[box]
            ):
                self._place(row, col, digit, box)
                if self._backtrack(row, col + 1):
                    return True
                self._unplace(row, col, digit, box)
        return False

    def _place(self, row: int, col: int, digit: str, box: int) -> None:
        self.board[row][col] = digit
        self._rows[row].add(digit)
        self._cols[col].add(digit)
        self._boxes[box].add(digit)

    def _unplace(self, row: int, col: int, digit: str, box: int) -> None:
        self.board[row][col] = self.EMPTY
        self._rows[row].remove(digit)
        self._cols[col].remove(digit)
        self._boxes[box].remove(digit)

    def _initialize_state(self) -> None:
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                value = self.board[r][c]
                if value != self.EMPTY:
                    self._rows[r].add(value)
                    self._cols[c].add(value)
                    self._boxes[self._box_index(r, c)].add(value)

    def _is_currently_valid(self) -> bool:
        rows: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        cols: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        boxes: List[set[str]] = [set() for _ in range(self.BOARD_SIZE)]
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                value = self.board[r][c]
                if value == self.EMPTY:
                    continue
                box = self._box_index(r, c)
                if value in rows[r] or value in cols[c] or value in boxes[box]:
                    return False
                rows[r].add(value)
                cols[c].add(value)
                boxes[box].add(value)
        return True

    @classmethod
    def _box_index(cls, row: int, col: int) -> int:
        return (row // cls.BOX_SIZE) * cls.BOX_SIZE + col // cls.BOX_SIZE

    @staticmethod
    def _has_valid_shape(board: Board) -> bool:
        return (
            isinstance(board, list)
            and len(board) == SudokuSolver.BOARD_SIZE
            and all(isinstance(row, list) and len(row) == SudokuSolver.BOARD_SIZE for row in board)
        )
