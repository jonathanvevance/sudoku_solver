import os
import sys
import pickle
import argparse
sys.path.append(r'C:\Users\user\Desktop\ML projects\sudoku_solver\Computer Vision')

from predict_sudoku import detect_board
from solver import solve_sudoku

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imgpath", required = True, help = 'image file path')
args = vars(ap.parse_args())


def print_sudoku(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[int(x) if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")


curdir = os.getcwd()
sudoku_model_pkl = os.path.join(curdir, 'Computer Vision/sudoku_model.pkl')
sudoku_model = pickle.load(open(sudoku_model_pkl, 'rb'))

board = detect_board(args['imgpath'], sudoku_model)
print('\nBoard detected: ')
print_sudoku(board)

try:
    solution = solve_sudoku(board)
    print('\nSOLUTION: ')
    print_sudoku(solution)
else:
    prunt('\nDetected board is not a valid sudoku puzzle')


