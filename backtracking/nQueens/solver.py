class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self._solutions = []
        self._state = []

    def solve(self):
        """Return all distinct solutions"""
        self._state = []
        self._solutions = []
        self._search()
        return self._solutions

    def _is_valid_state(self) -> bool:
        """Return True if current state represents a complete solution"""
        return len(self._state) == self.n
    # finds a list of candidates that can be used to construct the next
    def _get_candidates(self) -> set[int]:
        """Returns columns available for the next queen with pruning attacked cells"""
        if not self._state:
            return set(range(self.n))

        # find the next position in the  to populate
        position = len(self._state)
        candidates = set(range(self.n))

        # prune down candidates that place the queen into attacks
        for row, col in enumerate(self._state):

            # discard the column index if it's occupied by a queen
            candidates.discard(col)
            dist = position - row
            # discard diagonals
            candidates.discard(col + dist)
            candidates.discard(col - dist)
        return candidates

    def _search(self) -> None:
        """Backtracking. Populates self._solution"""
        if self._is_valid_state():
            self._solutions.append(self._state_to_strings())
            return

        for candidate in self._get_candidates():
            self._state.append(candidate)
            self._search()
            self._state.pop()

    def _state_to_strings(self) ->  list[str]:
        """Convert the current state to the needed string format"""
        return ['.' * i + 'Q' + '.' * (self.n - i - 1) for i in self._state]

class Solution:
    """LeetCode adapter"""
    def solveNQueens(self, n: int) -> list[list[str]]:
        return NQueensSolver(n).solve()
