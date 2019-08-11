# input = numpy array of nans and numbers
# output = solution numpy array

import numpy as np
from copy import deepcopy
from collections import defaultdict

# no backtracking
# PUZZLE = np.array([[6, 9, 0, 7, 0, 0, 0, 8, 3],
#                    [8, 0, 5, 3, 0, 4, 0, 6, 0],
#                    [0, 4, 0, 6, 1, 0, 0, 2, 5],
#                    [0, 0, 6, 0, 8, 1, 2, 0, 9],
#                    [1, 0, 9, 0, 4, 0, 8, 0, 6],
#                    [4, 0, 2, 0, 3, 6, 5, 0, 0],
#                    [0, 6, 8, 0, 0, 5, 3, 0, 4],
#                    [0, 7, 0, 4, 0, 9, 6, 1, 0],
#                    [9, 1, 0, 8, 6, 0, 0, 5, 0]])


# backtracking (single level)
# PUZZLE = np.array([[7, 9, 0, 0, 0, 0, 3, 0, 0],
#                    [0, 0, 0, 0, 0, 6, 9, 0, 0],
#                    [8, 0, 0, 0, 3, 0, 0, 7, 6],
#                    [0, 0, 0, 0, 0, 5, 0, 0, 2],
#                    [0, 0, 5, 4, 1, 8, 7, 0, 0],
#                    [4, 0, 0, 7, 0, 0, 0, 0, 0],
#                    [6, 1, 0, 0, 9, 0, 0, 0, 8],
#                    [0, 0, 2, 3, 0, 0, 0, 0, 0],
#                    [0, 0, 9, 0, 0, 0, 0, 5, 4]])

# no backtracking
# PUZZLE = np.array([[0, 2, 6, 0, 0, 0, 8, 1, 0],
#                    [3, 0, 0, 7, 0, 8, 0, 0, 6],
#                    [4, 0, 0, 0, 5, 0, 0, 0, 7],
#                    [0, 5, 0, 1, 0, 7, 0, 9, 0],
#                    [0, 0, 3, 9, 0, 5, 1, 0, 0],
#                    [0, 4, 0, 3, 0, 2, 0, 5, 0],
#                    [1, 0, 0, 0, 3, 0, 0, 0, 2],
#                    [5, 0, 0, 2, 0, 4, 0, 0, 9],
#                    [0, 3, 8, 0, 0, 0, 4, 6, 0]])

# hard problem - nested backtracking
# PUZZLE = np.array([[0, 0, 0, 2, 0, 0, 0, 6, 3],
#                    [3, 0, 0, 0, 0, 5, 4, 0, 1],
#                    [0, 0, 1, 0, 0, 3, 9, 8, 0],
#                    [0, 0, 0, 0, 0, 0, 0, 9, 0],
#                    [0, 0, 0, 5, 3, 8, 0, 0, 0],
#                    [0, 3, 0, 0, 0, 0, 0, 0, 0],
#                    [0, 2, 6, 3, 0, 0, 5, 0, 0],
#                    [5, 0, 3, 7, 0, 0, 0, 0, 8],
#                    [4, 7, 0, 0, 0, 1, 0, 0, 0]])

# backtracking (single level)
# PUZZLE = np.array([[0, 0, 0, 0, 0, 0, 6, 8, 0],
#                    [0, 0, 0, 0, 7, 3, 0, 0, 9],
#                    [3, 0, 9, 0, 0, 0, 0, 4, 5],
#                    [4, 9, 0, 0, 0, 0, 0, 0, 0],
#                    [8, 0, 3, 0, 5, 0, 9, 0, 2],
#                    [0, 0, 0, 0, 0, 0, 0, 3, 6],
#                    [9, 6, 0, 0, 0, 0, 3, 0, 8],
#                    [7, 0, 0, 6, 8, 0, 0, 0, 0],
#                    [0, 2, 8, 0, 0, 0, 0, 0, 0]])

# hardest SUDOKU in the world
PUZZLE = np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 3, 6, 0, 0, 0, 0, 0],
                   [0, 7, 0, 0, 9, 0, 2, 0, 0],
                   [0, 5, 0, 0, 0, 7, 0, 0, 0],
                   [0, 0, 0, 0, 4, 5, 7, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 3, 0],
                   [0, 0, 1, 0, 0, 0, 0, 6, 8],
                   [0, 0, 8, 5, 0, 0, 0, 1, 0],
                   [0, 9, 0, 0, 0, 0, 4, 0, 0]])

def get_filled_nums_dicts(puzzle):

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

    print('\nProblem\n')
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j], end = '   ')
        print('\n')

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

        if(back_tracking_req == 1): # requires backtracking

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

    print('\nSolution\n')
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j], end = '   ')
        print('\n')


def main():

    # PUZZLE = np.zeros([9,9], dtype = int)
    # for i in range(9):
    #     for j in range(9):
    #         num = int(input(f'enter num at ({i+1},{j+1}): '))
    #         PUZZLE[i][j] = num

    solve_sudoku(PUZZLE)


if __name__ == '__main__':
    main()