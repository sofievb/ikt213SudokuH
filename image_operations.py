import cv2 as cv


def show_img(image_name, image, debug):
    if debug:
        cv.imshow(image_name, image)
        cv.waitKey(0)
        cv.destroyAllWindows()


def canny_edge_detection(image, threshold_1, threshold_2, k):
    blur_image = cv.GaussianBlur(image, (k, k), 3)
    canny_image = cv.Canny(blur_image, threshold_1, threshold_2)
    return canny_image


def thresholding(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur_image = cv.GaussianBlur(gray_image, (3, 3), 3)
    thresh = cv.adaptiveThreshold(blur_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    thresh = cv.bitwise_not(thresh)
    return thresh


def find_contours(image):
    contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours
