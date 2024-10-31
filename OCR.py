import cv2 as cv
import numpy as np
import pytesseract
from image_operations import thresholding, find_contours, show_img

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseractOCR\tesseract.exe'

def find_xy(cell, crop):
    x, y = cell.shape[0], cell.shape[1]
    x0 = int(x / crop)
    y0 = int(y / crop)
    x1 = x - x0
    y1 = y - y0
    return x0, y0, x1, y1


def masked_digit(cell):
    debug = False
    x0, y0, x1, y1 = find_xy(cell, 10)
    cropped_cell = cell[x0:x1, y0:y1]

    thresh = thresholding(cropped_cell)
    show_img('thresh_cell', thresh, debug)

    contours = find_contours(thresh)
    largest_contour = None
    max_area = 0

    if len(contours) == 0:
        return None
    else:
        for contour in contours:
            area = cv.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        (height, width) = thresh.shape

        if largest_contour is not None:

            mask = np.zeros(thresh.shape, dtype="uint8")
            cv.drawContours(mask, [largest_contour], -1, 255, -1)

            filled = cv.countNonZero(mask) / float(height * width)
            if filled < 0.04:
                return None

            digit = cv.bitwise_and(thresh, thresh, mask=mask)

            return digit
    return None


def erosion(image, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded_image = cv.erode(image, kernel, iterations=1)
    return eroded_image


def dilation(image, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_image = cv.dilate(image, kernel, iterations=1)
    return dilated_image


def OCR(masked):
    show_img('image_for_OCR', masked, False)

    options = "--psm 6 -c tessedit_char_whitelist=123456789"
    digit = pytesseract.image_to_string(masked, config=options)

    #print(digit)
    if digit == '':
        digit = 0

    return digit


def find_digit(cell):
    debug = False
    masked = masked_digit(cell)

    if masked is not None:
        show_img('sudoku_masked', masked, debug)
        eroded_image = erosion(masked, 3)
        show_img('eroded', eroded_image, debug)
        dilated_image = dilation(eroded_image, 3)
        show_img('dilated', dilated_image, debug)
        digit = OCR(dilated_image)
        if digit == 0:
            digit = OCR(masked)

    else:
        digit = 0
    return digit


def find_board(cells):
    n = 0
    board = np.zeros((9, 9), dtype="int")

    for x in range(0,9):
        for y in range(0, 9):
            digit = find_digit(cells[n])
            board[x][y] = digit
            n += 1

    return board
