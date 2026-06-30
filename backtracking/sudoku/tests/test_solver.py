"""Tests for SudokuSolver."""

import copy
import unittest

from backtracking.sudoku.solver import SudokuSolver


# A standard easy puzzle and its solution.
EASY_PUZZLE = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

EASY_SOLUTION = [
    ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
    ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
    ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
]

EMPTY_BOARD = [["." for _ in range(9)] for _ in range(9)]


class TestSudokuSolver(unittest.TestCase):
    """Tests for the core behavior of SudokuSolver."""

    def test_solves_easy_puzzle_in_place(self):
        board = copy.deepcopy(EASY_PUZZLE)
        solver = SudokuSolver(board)
        result = solver.solve()
        self.assertTrue(result)
        self.assertEqual(board, EASY_SOLUTION)

    def test_is_solved_true_after_solving(self):
        board = copy.deepcopy(EASY_PUZZLE)
        solver = SudokuSolver(board)
        solver.solve()
        self.assertTrue(solver.is_solved())

    def test_is_solved_false_before_solving(self):
        solver = SudokuSolver(copy.deepcopy(EASY_PUZZLE))
        self.assertFalse(solver.is_solved())

    def test_count_empty_decreases_to_zero(self):
        board = copy.deepcopy(EASY_PUZZLE)
        solver = SudokuSolver(board)
        empty_before = solver.count_empty()
        self.assertGreater(empty_before, 0)
        solver.solve()
        self.assertEqual(solver.count_empty(), 0)

    def test_is_valid_board_on_input(self):
        solver = SudokuSolver(copy.deepcopy(EASY_PUZZLE))
        self.assertTrue(solver.is_valid_board())

    def test_is_valid_board_detects_row_conflict(self):
        broken = copy.deepcopy(EASY_PUZZLE)
        broken[0][2] = "5"  # duplicate '5' in row 0
        solver = SudokuSolver(broken)
        self.assertFalse(solver.is_valid_board())

    def test_solves_empty_board(self):
        board = [row[:] for row in EMPTY_BOARD]
        solver = SudokuSolver(board)
        self.assertTrue(solver.solve())
        self.assertTrue(solver.is_solved())

    def test_raises_on_wrong_shape(self):
        bad = [["." for _ in range(8)] for _ in range(9)]  # 9x8 instead of 9x9
        with self.assertRaises(ValueError):
            SudokuSolver(bad)

    def test_str_contains_separators(self):
        solver = SudokuSolver(copy.deepcopy(EASY_PUZZLE))
        rendered = str(solver)
        self.assertIn("|", rendered)
        self.assertIn("-", rendered)

    def test_repr_shows_empty_count(self):
        solver = SudokuSolver(copy.deepcopy(EASY_PUZZLE))
        self.assertIn("empty_cells=", repr(solver))


if __name__ == "main":
    unittest.main()