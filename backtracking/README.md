# Sudoku Solver

Backtracking-based solver for the classic 9x9 Sudoku puzzle.

## Problem

[LeetCode 37 — Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) (Hard).

Fill a partially-completed 9x9 grid so that every row, column, and 3x3 box contains
the digits 1–9 exactly once. Empty cells are marked with ..

## Approach

Backtracking with incremental state tracking.

Instead of re-validating placement against the whole row, column, and box every time
(which would be O(n) per check), the solver maintains three sets of seen digits — one
per row, one per column, one per 3x3 box. Validity becomes an O(1) set membership test.

On each placement, the digit is added to the corresponding three sets; on backtrack,
it's removed. This keeps the invariant correct across the entire search tree.

## Complexity

- Time: O(9^k) in the worst case, where k is the number of empty cells.
  In practice much faster due to constraint propagation through the row/col/box sets.
- Space: O(1) — the board and the three sets are all fixed-size (9 elements each).

## Public API

| Method            | Returns | Description                                              |
|-------------------|---------|----------------------------------------------------------|
| solve()           | bool    | Solve the puzzle in place. Returns False if unsolvable.  |
| is_solved()       | bool    | True if the board is fully filled and valid.             |
| is_valid_board()  | bool    | True if the current state has no row/col/box conflicts.  |
| count_empty()     | int     | Number of empty cells remaining.                         |
| `__str__`()       | str     | Human-readable board with 3x3 box separators.            |

## Usage

```python
from backtracking.sudoku.solver import SudokuSolver

board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    # ... 8 more rows
]

solver = SudokuSolver(board)
solver.solve()
print(solver)
```

## Tests

Run the test suite from the project root:

```bash
python3 -m unittest backtracking.sudoku.tests.test_solver -v
```

10 tests covering: solving correctness, in-place modification, conflict detection,
empty-board handling, shape validation, and string representation.

## Notes

- The board is modified __in place__. If you need to preserve the input,
  pass a copy.deepcopy of it.
- The solver does not verify that the input has a unique solution.
  It returns the first solution found.
