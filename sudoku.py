import numpy as np
from copy import deepcopy
from collections import defaultdict


def get_filled_nums_dicts(puzzle):
    """
    METHOD THAT GIVES THREE DICTIONARIES OF NUMBERS INITIALLY FILLED IN, IN ANY ROW, COLUMN OR SQUARE.

    Arguments:
        puzzle                  : 2d numpy array of zeros for unknown numbers and integers 1-9

    Returns:
        nums_in_row_dict        : dict giving the list of numbers initially filled in each row -
                                  indexed by 0-9 integers
        nums_in_col_dict        : dict giving the list of numbers initially filled in each column -
                                  indexed by 0-9 integers
        nums_in_square_dict     : dict giving the list of numbers initially filled in each square -
                                  indexed by row_index, col_index for each big square
    """   

    nums_in_row_dict = defaultdict(set)
    nums_in_col_dict = defaultdict(set)
    nums_in_square_dict = defaultdict(set)

    for row in range(9):
        for col in range(9):

            if(puzzle[row][col] != 0):
                nums_in_row_dict[row].add(puzzle[row][col])
                nums_in_col_dict[col].add(puzzle[row][col])

                square_row_idx = (row // 3)
                square_col_idx = (col // 3)
                nums_in_square_dict[(square_row_idx, square_col_idx)].add(puzzle[row][col])

    return nums_in_row_dict, nums_in_col_dict, nums_in_square_dict


def update_possible_nums_dict(puzzle, row, col, possible_nums_dict):
    """
    METHOD UPDATES THE POSSIBLE NUMBERS DICTIONARY, BY REMOVING THE NUMBER ADDED AT (ROW, COL) FROM THE LIST
    OF POSSIBLE NUMBERS AT EACH SQUARE IN THAT PARTICULAR ROW, COLUMN AND SQUARE

    Arguments:
        puzzle              : 2d numpy array of zeros for unknown numbers and integers 1-9
        row                 : index of row where a number was added
        col                 : index of column where a number was added
        possible_nums_dict  : dict which gives list of possible numbers in each square - indexed by (row index, col index)

    Returns : None
    """
    num_added = puzzle[row][col]

    for i in range(9):
        if(possible_nums_dict.get((i, col)) != None):
            possible_nums_dict[(i, col)].discard(num_added)

    for j in range(9):
        if(possible_nums_dict.get((row, j)) != None):
            possible_nums_dict[(row, j)].discard(num_added)

    square_row_index = (row // 3)
    square_col_index = (col // 3)
    for i in range(3 * square_row_index, 3 * square_row_index + 3):
        for j in range(3 * square_col_index, 3 * square_col_index + 3):

            if(possible_nums_dict.get((i, j)) != None):
                possible_nums_dict[(i, j)].discard(num_added)


def get_initial_possible_nums_dict(puzzle,
                                   nums_in_row_dict,
                                   nums_in_col_dict,
                                   nums_in_square_dict):

    """
    METHOD THAT INITIALIZES THE POSSIBLE NUMBERS DICT BASED ON THE NUMBERS KNOWN INITIALLY

    Arguments:
        puzzle                  : 2d numpy array of zeros for unknown numbers and integers 1-9
        nums_in_row_dict        : dict giving the list of numbers initially filled in each row -
                                  indexed by 0-9 integers
        nums_in_col_dict        : dict giving the list of numbers initially filled in each column -
                                  indexed by 0-9 integers
        nums_in_square_dict     : dict giving the list of numbers initially filled in each square -
                                  indexed by row_index, col_index for each big square
    Returns:
        possible_nums_dict : dict which gives list of possible numbers in each square - indexed by (row index, col index)
    """
    all_nums_set = set(range(1, 10))
    possible_nums_dict = dict()
    for i in range(9):
        for j in range(9):

            if(puzzle[i][j] == 0):

                square_row_idx = (i // 3)
                square_col_idx = (j // 3)

                invalid_nums_set = nums_in_row_dict[i].union(nums_in_col_dict[j])
                invalid_nums_set = invalid_nums_set.union(nums_in_square_dict[(square_row_idx, square_col_idx)])

                possible_nums_dict[(i, j)] = all_nums_set - invalid_nums_set

    return possible_nums_dict


def solve_sudoku(puzzle):

    """
    METHOD THAT RETURNS THE SOLVED SUDOKU PUZZLE

    Arguments:
        puzzle             : 2d numpy array of zeros for unknown numbers and integers 1-9

    Returns:
        puzzle (MODIFIED)  : 2d numpy array with integers 1-9
    """

    (nums_in_row_dict,
     nums_in_col_dict,
     nums_in_square_dict) = get_filled_nums_dicts(puzzle)

    possible_nums_dict = get_initial_possible_nums_dict(puzzle,
                                                        nums_in_row_dict,
                                                        nums_in_col_dict,
                                                        nums_in_square_dict)

    backtracking_dicts_list = []
    backtracking_nodes_list = []
    while len(possible_nums_dict) > 0:

        back_tracking_req = 1
        index_tuples_list = list(possible_nums_dict.keys())
        for index_tuple in index_tuples_list:

            possible_nums_set = possible_nums_dict.get(index_tuple)

            if len(possible_nums_set) == 0:
            # go to previous node and take a new branch, or delete the last node if all branches have been checked

                last_backtracking_dict = backtracking_dicts_list[-1]

                puzzle               = deepcopy(last_backtracking_dict['puzzle'])
                row_try              = last_backtracking_dict['row_try']
                col_try              = last_backtracking_dict['col_try']
                num_try              = last_backtracking_dict['num_try']
                possible_nums_dict   = deepcopy(last_backtracking_dict['possible_nums_dict'])

                possible_nums_dict.get((row_try, col_try)).discard(num_try)
                last_backtracking_dict['possible_nums_dict'].get((row_try, col_try)).discard(num_try)

                if len(possible_nums_dict.get((row_try, col_try))) > 0:
                    last_backtracking_dict['num_try'] = max(possible_nums_dict.get((row_try, col_try)))

                    if len(possible_nums_dict.get((row_try, col_try))) == 1:
                        backtracking_dicts_list = backtracking_dicts_list[:-1]
                        backtracking_nodes_list = backtracking_nodes_list[:-1]

                else:
                    backtracking_dicts_list = backtracking_dicts_list[:-1]
                    backtracking_nodes_list = backtracking_nodes_list[:-1]

                back_tracking_req = 0
                break

            if len(possible_nums_set) == 1:

                back_tracking_req = 0
                row, col = index_tuple
                (num, ) = possible_nums_set
                puzzle[row][col] = num

                update_possible_nums_dict(puzzle, row, col, possible_nums_dict)

                del possible_nums_dict[(row, col)]

        if(back_tracking_req == 1):
        # set the current position as backtracking node

            backtracking_dict = dict()
            row_try, col_try = min(possible_nums_dict, key = possible_nums_dict.get)
            num_try = max(possible_nums_dict.get((row_try, col_try)))
            # just getting some element - here, max

            if (row_try, col_try) not in backtracking_nodes_list:

                puzzle_copy = deepcopy(puzzle)
                possible_nums_dict_copy = deepcopy(possible_nums_dict)

                backtracking_dict['puzzle']               = puzzle_copy
                backtracking_dict['num_try']              = num_try
                backtracking_dict['row_try']              = row_try
                backtracking_dict['col_try']              = col_try
                backtracking_dict['possible_nums_dict']   = possible_nums_dict_copy

                backtracking_nodes_list.append((row_try, col_try))
                backtracking_dicts_list.append(backtracking_dict)

            puzzle[row_try][col_try] = num_try

            update_possible_nums_dict(puzzle, row_try, col_try, possible_nums_dict)
            del possible_nums_dict[(row_try, col_try)]

    return puzzle

def main():

    PUZZLE = np.zeros([9,9], dtype = int)
    for i in range(9):
        for j in range(9):
            num = int(input(f'enter num at ({i+1},{j+1}): '))
            PUZZLE[i][j] = num

    print('\nProblem\n')
    for i in range(9):
        for j in range(9):
            print(PUZZLE[i][j], end = '   ')
        print('\n')

    solution = solve_sudoku(PUZZLE)

    print('\nSolution\n')
    for i in range(9):
        for j in range(9):
            print(solution[i][j], end = '   ')
        print('\n')



if __name__ == '__main__':
    main()


