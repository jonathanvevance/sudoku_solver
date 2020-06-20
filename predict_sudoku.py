import os
import sys
import cv2
import pickle
import numpy as np
from detect_sudoku import (find_grid_in_img,
                           center_image_single_contour,
                           center_image_broken_contours)


linewidth = 4
square_size = 28
total_square_size = square_size + 2 * linewidth


def detect_board(img_file_path, sudoku_model):

    img = cv2.imread(img_file_path, 0)
    try:
        grid = find_grid_in_img(img)
    except:
        sys.exit('Sudoku not detected')

    sudoku = np.zeros((9,9))
    for i in range(9):
        for j in range(9):

            square = grid[i*total_square_size: (i+1)*total_square_size,
                        j*total_square_size: (j+1)*total_square_size]

            square = square[linewidth: -linewidth, linewidth: -linewidth]
            centered = center_image_single_contour(square)

            if not isinstance(centered, np.ndarray):
                centered = center_image_broken_contours(square)

            if isinstance(centered, np.ndarray):

                centered_exp = centered / 255.0
                centered_exp = centered_exp.ravel()
                centered_exp = np.expand_dims(centered_exp, 0)
                digit = sudoku_model.predict(centered_exp)[0]
                sudoku[i][j] = digit

    return sudoku




