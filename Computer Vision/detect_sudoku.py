import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist

linewidth = 4
square_size = 28
adaptive_C_1 = 2
adaptive_C_2 = 15
blur_strength_1 = 5
blur_strength_2 = 5
adaptive_blocksize_1 = 11
adaptive_blocksize_2 = 21
contour_area_threshold = 30 # 50

def order_points(corners):

    points = []
    for idx in range(corners.shape[0]):
        points.append(corners[idx][0])

    xSorted = sorted(points, key = lambda x: x[1])
    leftMost = xSorted[:2]
    rightMost = xSorted[2:]
    if leftMost[0][0] > leftMost[1][0]:
        (bl, tl) = leftMost
    else:
        (tl, bl) = leftMost

    D = dist.cdist(tl[np.newaxis], rightMost.copy(), "euclidean")[0]

    if D[0] > D[1]:
        (br, tr) = rightMost
    else:
        (tr, br) = rightMost
    return np.array([tl, tr, br, bl], dtype="float32")

def find_grid_in_img(img):

    blurred = cv2.medianBlur(img, blur_strength_1)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, adaptive_blocksize_1, adaptive_C_1)

    blurred_again = cv2.medianBlur(thresholded, blur_strength_1)
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3)) # cross pattern kernel
    thickened = cv2.erode(blurred_again, cross_kernel, iterations = 1)


    thickened_inv = cv2.bitwise_not(thickened)
    contours, __ = cv2.findContours(thickened_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key = cv2.contourArea)

    epsilon = 0.1 * cv2.arcLength(max_contour, True)
    contour_corners = cv2.approxPolyDP(max_contour, epsilon, True)
    contour_corners = order_points(contour_corners)

    l, b = img.shape
    image_corners = [[0, 0], [0, b], [l, b], [l, 0]]
    image_corners = np.float32(image_corners)

    matrix = cv2.getPerspectiveTransform(contour_corners, image_corners)
    grid = cv2.warpPerspective(img, matrix, img.shape)

    total_square_size = square_size + 2 * linewidth
    grid = cv2.resize(grid, (total_square_size * 9, total_square_size * 9))
    grid = cv2.adaptiveThreshold(grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, adaptive_blocksize_2, adaptive_C_2)

    grid = cv2.bitwise_not(grid)
    return grid

def center_image_single_contour(square):

    contours, __ = cv2.findContours(square, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        max_contour = max(contours, key = cv2.contourArea)
        if cv2.contourArea(max_contour) > contour_area_threshold:
            x, y, w, h = cv2.boundingRect(max_contour)
            x_center = square_size // 2
            y_center = square_size // 2

            centered = np.zeros((square_size, square_size), dtype = 'float32')
            (centered[y_center - int(np.ceil(h / 2)) : y_center + h // 2,
                    x_center - int(np.ceil(w / 2)) : x_center + w // 2]) = square[y : y + h, x : x + w]

            return centered
    except: return None

def center_image_broken_contours(square):

    contours, __ = cv2.findContours(square, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
        total_area = np.sum([cv2.contourArea(cnt) for cnt in valid_contours])
        if total_area > contour_area_threshold:

            max_x = max_y = 0
            min_x = min_y = square.shape[0]
            for contour in valid_contours:
                x, y, w, h = cv2.boundingRect(contour)
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x + w > max_x:
                    max_x = x + w
                if y + h > max_y:
                    max_y = y + h

            x_center = square_size // 2
            y_center = square_size // 2

            (x, y, w, h) = (min_x, min_y, max_x - min_x, max_y - min_y)
            centered = np.zeros((square_size, square_size), dtype = 'float32')
            (centered[y_center - int(np.ceil(h / 2)) : y_center + h // 2,
                    x_center - int(np.ceil(w / 2)) : x_center + w // 2]) = square[y : y + h, x : x + w]

            return centered
    except: return None

# def detect_digit(square):

#     crop = square[linewidth: -linewidth, linewidth: -linewidth]
#     crop_uint32 = crop.astype(np.uint8)
#     contours, __ = cv2.findContours(crop_uint32, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     try:
#         max_contour = max(contours, key = cv2.contourArea)
#         if cv2.contourArea(max_contour) > contour_area_threshold:
#             return crop
#         else:
#             return None
#     except:
#         return None


