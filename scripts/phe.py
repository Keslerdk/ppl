import urllib.request as urllib2
import numpy as np
import cv2
import time
import math

numbers=list(map(int, input().split()))
def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread('vid_s_clevera.png')
viewImage(img, 'img')
mask = cv2.inRange(img, (numbers[0], numbers[1], numbers[2]), (numbers[3], numbers[4], numbers[5]))
viewImage(mask, 'mask')


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def get_aoi(img):
    rows, cols = img.shape[:2]
    mask = np.zeros_like(img)

    left_bottom = [cols * 0.35, rows * 0]
    right_bottom = [cols * 0.65, rows * 0]
    left_top = [cols * 0.35, rows]
    right_top = [cols * 0.65, rows]

    vertices = np.array([[left_bottom, left_top, right_top, right_bottom]], dtype=np.int32)

    if len(mask.shape) == 2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,) * mask.shape[2])
    return cv2.bitwise_and(img, mask)


def get_hough_lines(img, rho=1, theta=np.pi / 180, threshold=50, min_line_len=100, max_line_gap=40):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                            minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    print(lines)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, 3)
            if y1 <= 119 <= y2 or y2 <= 119 <= y1:
                b = (y2 * x1 - y1 * x2) / (x1 - x2)
                k = (y1 - b) / x1
                y = 119
                x = int((y - b) / k)
                if y1 < y2:
                    if y - y1 >= 30:
                        x0 = int((89 - b) / k)
                        print(x0)
                        cv2.line(img, (x, 119), (x, 89), (0, 0, 255), 2)
                        cv2.line(img, (x, 89), (x0, 89), (0, 0, 255), 2)
                        cv2.line(img, (x, 119), (x0, 89), (0, 255, 0), 2)
                        # viewImage(img, 'hgc')
                        tg = abs(x0 - x) / 30
                        arctg = math.atan(tg)
                        print(arctg)
                else:
                    if y - y2 >= 30:
                        x0 = int((89 - b) / k)
                        print(x0)
                        cv2.line(img, (x, 119), (x, 89), (0, 0, 255), 2)
                        cv2.line(img, (x, 89), (x0, 89), (0, 0, 255), 2)
                        cv2.line(img, (x, 119), (x0, 89), (0, 255, 0), 2)
                        # viewImage(img, 'hgc')
                        tg = abs(x0 - x) / 30
                        arctg = math.atan(tg)
                        print(arctg)
    return img
def mask(img, numbers):
    mask = cv2.inRange(img, (numbers[0], numbers[1], numbers[2]), (numbers[3], numbers[4], numbers[5]))
    blurred_img = gaussian_blur(mask, kernel_size=7)
    viewImage(blurred_img, 'blury')
    canny_img = canny(blurred_img, low_threshold=70, high_threshold=140)
    viewImage(canny_img, 'canny')
    aoi_img = get_aoi(canny_img)
    viewImage(aoi_img, 'bli')
    line = get_hough_lines(aoi_img)
    try:
        hough_lines_img = (draw_lines(img, line))
    except:
        return img
    else:
        #print(yaw(line))
        return hough_lines_img
