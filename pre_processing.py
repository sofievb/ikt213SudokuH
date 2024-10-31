import cv2 as cv
import numpy as np
from image_operations import find_contours, canny_edge_detection, show_img


def find_sudoku(image, edged):
    contours = find_contours(edged)

    largest_contour = None
    max_area = 0

    for contour in contours:
        # Approximate the contour with a polygon
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # Check if the contour has four corners
        if len(approx) == 4:
            # Calculate the area of the contour
            area = cv.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

    sudoku_frame = cv.drawContours(image, largest_contour, -1, (0, 255, 0), 4)

    return sudoku_frame, largest_contour


def birdseye_view(image, contour):
    epsilon = 0.02 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)
    corners = approx.reshape(-1, 2)

    # Sort the corners to ensure they are in the correct order
    corners = sorted(corners, key=lambda x: x[0])

    # Check the y-coordinate to determine the top and bottom corners
    if corners[0][1] < corners[1][1]:
        top_left, bottom_left = corners[0], corners[1]
    else:
        top_left, bottom_left = corners[1], corners[0]

    if corners[2][1] < corners[3][1]:
        top_right, bottom_right = corners[2], corners[3]
    else:
        top_right, bottom_right = corners[3], corners[2]

    width, height = 600, 600

    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype='float32')

    src_points = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

    transformation_matrix = cv.getPerspectiveTransform(src_points, dst_points)

    birdseye_sudoku = cv.warpPerspective(image, transformation_matrix, (width, height))

    return birdseye_sudoku


def find_cells(image):
    debug = False
    img_canny = canny_edge_detection(image, 50, 50, 7)
    show_img('sudoku_canny', img_canny, debug)

    img_contour, contour = find_sudoku(image, img_canny)
    show_img('sudoku_contour', img_contour, debug)

    img_ready = birdseye_view(image, contour)
    show_img('sudoku_ready', img_ready, debug)
    cell_size = img_ready.shape[0] // 9
    cells = []
    cell_coord = []

    for i in range(9):
        row_coord = []
        for j in range(9):
            x_start = j * cell_size
            x_end = (j + 1) * cell_size
            y_start = i * cell_size
            y_end = (i + 1) * cell_size

            cell = img_ready[y_start:y_end, x_start:x_end]
            cells.append(cell)
            row_coord.append((x_start, y_start))
        cell_coord.append(row_coord)
    for cell in cells:
        show_img('sudoku_cell', cell, debug)

    return cells,cell_coord,cell_size,img_ready
