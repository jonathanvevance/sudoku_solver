import unittest
import sudoku
import numpy as np

class sudoku_test(unittest.TestCase):

    def test_simple_puzzle(self):

        puzzle = np.array([[6, 9, 0, 7, 0, 0, 0, 8, 3],
                           [8, 0, 5, 3, 0, 4, 0, 6, 0],
                           [0, 4, 0, 6, 1, 0, 0, 2, 5],
                           [0, 0, 6, 0, 8, 1, 2, 0, 9],
                           [1, 0, 9, 0, 4, 0, 8, 0, 6],
                           [4, 0, 2, 0, 3, 6, 5, 0, 0],
                           [0, 6, 8, 0, 0, 5, 3, 0, 4],
                           [0, 7, 0, 4, 0, 9, 6, 1, 0],
                           [9, 1, 0, 8, 6, 0, 0, 5, 0]])

        expected_answer = np.array([[6, 9, 1, 7, 5, 2, 4, 8, 3],
                                    [8, 2, 5, 3, 9, 4, 1, 6, 7],
                                    [3, 4, 7, 6, 1, 8, 9, 2, 5],
                                    [7, 3, 6, 5, 8, 1, 2, 4, 9],
                                    [1, 5, 9, 2, 4, 7, 8, 3, 6],
                                    [4, 8, 2, 9, 3, 6, 5, 7, 1],
                                    [2, 6, 8, 1, 7, 5, 3, 9, 4],
                                    [5, 7, 3, 4, 2, 9, 6, 1, 8],
                                    [9, 1, 4, 8, 6, 3, 7, 5, 2]])

        actual_answer = sudoku.solve_sudoku(puzzle)
        self.assertTrue(np.array_equal(expected_answer, actual_answer))

    def test_single_backtracking(self):

        puzzle = np.array([[7, 9, 0, 0, 0, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 6, 9, 0, 0],
                           [8, 0, 0, 0, 3, 0, 0, 7, 6],
                           [0, 0, 0, 0, 0, 5, 0, 0, 2],
                           [0, 0, 5, 4, 1, 8, 7, 0, 0],
                           [4, 0, 0, 7, 0, 0, 0, 0, 0],
                           [6, 1, 0, 0, 9, 0, 0, 0, 8],
                           [0, 0, 2, 3, 0, 0, 0, 0, 0],
                           [0, 0, 9, 0, 0, 0, 0, 5, 4]])

        expected_answer = np.array([[7, 9, 6, 8, 5, 4, 3, 2, 1],
                                    [2, 4, 3, 1, 7, 6, 9, 8, 5],
                                    [8, 5, 1, 2, 3, 9, 4, 7, 6],
                                    [1, 3, 7, 9, 6, 5, 8, 4, 2],
                                    [9, 2, 5, 4, 1, 8, 7, 6, 3],
                                    [4, 6, 8, 7, 2, 3, 5, 1, 9],
                                    [6, 1, 4, 5, 9, 7, 2, 3, 8],
                                    [5, 8, 2, 3, 4, 1, 6, 9, 7],
                                    [3, 7, 9, 6, 8, 2, 1, 5, 4]])

        actual_answer = sudoku.solve_sudoku(puzzle)
        self.assertTrue(np.array_equal(expected_answer, actual_answer))

    def test_multiple_backtracking(self):

        puzzle = np.array([[0, 0, 0, 2, 0, 0, 0, 6, 3],
                           [3, 0, 0, 0, 0, 5, 4, 0, 1],
                           [0, 0, 1, 0, 0, 3, 9, 8, 0],
                           [0, 0, 0, 0, 0, 0, 0, 9, 0],
                           [0, 0, 0, 5, 3, 8, 0, 0, 0],
                           [0, 3, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 6, 3, 0, 0, 5, 0, 0],
                           [5, 0, 3, 7, 0, 0, 0, 0, 8],
                           [4, 7, 0, 0, 0, 1, 0, 0, 0]])

        expected_answer = np.array([[8, 5, 4, 2, 1, 9, 7, 6, 3],
                                    [3, 9, 7, 8, 6, 5, 4, 2, 1],
                                    [2, 6, 1, 4, 7, 3, 9, 8, 5],
                                    [7, 8, 5, 1, 2, 6, 3, 9, 4],
                                    [6, 4, 9, 5, 3, 8, 1, 7, 2],
                                    [1, 3, 2, 9, 4, 7, 8, 5, 6],
                                    [9, 2, 6, 3, 8, 4, 5, 1, 7],
                                    [5, 1, 3, 7, 9, 2, 6, 4, 8],
                                    [4, 7, 8, 6, 5, 1, 2, 3, 9]])

        actual_answer = sudoku.solve_sudoku(puzzle)
        self.assertTrue(np.array_equal(expected_answer, actual_answer))

    def test_hardest_sudoku(self):

        puzzle = np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 6, 0, 0, 0, 0, 0],
                           [0, 7, 0, 0, 9, 0, 2, 0, 0],
                           [0, 5, 0, 0, 0, 7, 0, 0, 0],
                           [0, 0, 0, 0, 4, 5, 7, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0, 3, 0],
                           [0, 0, 1, 0, 0, 0, 0, 6, 8],
                           [0, 0, 8, 5, 0, 0, 0, 1, 0],
                           [0, 9, 0, 0, 0, 0, 4, 0, 0]])

        expected_answer = np.array([[8, 1, 2, 7, 5, 3, 6, 4, 9],
                                    [9, 4, 3, 6, 8, 2, 1, 7, 5],
                                    [6, 7, 5, 4, 9, 1, 2, 8, 3],
                                    [1, 5, 4, 2, 3, 7, 8, 9, 6],
                                    [3, 6, 9, 8, 4, 5, 7, 2, 1],
                                    [2, 8, 7, 1, 6, 9, 5, 3, 4],
                                    [5, 2, 1, 9, 7, 4, 3, 6, 8],
                                    [4, 3, 8, 5, 2, 6, 9, 1, 7],
                                    [7, 9, 6, 3, 1, 8, 4, 5, 2]])

        actual_answer = sudoku.solve_sudoku(puzzle)
        self.assertTrue(np.array_equal(expected_answer, actual_answer))


if __name__ == "__main__":
    unittest.main()

