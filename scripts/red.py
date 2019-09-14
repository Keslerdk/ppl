import urllib.request as urllib2
import numpy as np
import cv2
import time
import math
line=[]

def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def isolate_color_mask(img, low_thresh, high_thresh):
    assert (low_thresh.all() >= 0 and low_thresh.all() <= 255)
    assert (high_thresh.all() >= 0 and high_thresh.all() <= 255)
    return cv2.inRange(img, low_thresh, high_thresh)


def to_hls(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)


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


def get_raw():
    request = urllib2.Request('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
    raw = []
    try:
        time.sleep(15)
        arr = np.asarray(bytearray(urllib2.urlopen(request).read()), dtype=np.uint8)
    except:
        time.sleep(0.5)
        raw = get_raw()
    else:
        raw = cv2.imdecode(arr, -1)
    return raw


def yaw(lines):
    for line in lines:
         for x1, y1, x2, y2 in line:
             if y1 <= 119 <= y2 or y2 <= 119 <= y1:
                 b = (y2 * x1 - y1 * x2) / (x1 - x2)
                 k = (y1 - b) / x1
                 y = 119
                 x = int((y - b) / k)
                 if y1 < y2:
                     if y - y1 >= 30:
                         x0 = int((89 - b) / k)
                         tg = abs(x0 - x) / 30
                         arctg = math.atan(tg)
                         return arctg
                 else:
                     if y - y2 >= 30:
                         x0 = int((89 - b) / k)
                         tg = abs(x0 - x) / 30
                         arctg = math.atan(tg)
                         return -arctg


img = get_raw()
cv2.imwrite('vid_s_clevera.png', img)
#img = cv2.imread('vid_s_clevera.png')
viewImage(img, 'img')


def linii(img):
    global line
    gray_img = grayscale(img)
    viewImage(gray_img, 'gray')
    darkened_img = adjust_gamma(gray_img, 0.5)
    cv2.imwrite('dark.png', darkened_img)
    # equ = cv2.equalizeHist(darkened_img)
    viewImage(darkened_img, 'dark')
    # viewImage(equ, 'vnj')
    white_masks = []
    yellow_masks = []
    white_masks = isolate_color_mask(to_hls(img), np.array([0, 103, 30], dtype=np.uint8),
                                     np.array([200, 200, 200], dtype=np.uint8))
    yellow_masks = isolate_color_mask(to_hls(img), np.array([10, 0, 100], dtype=np.uint8),
                                      np.array([40, 255, 255], dtype=np.uint8))
    mask = cv2.bitwise_or(white_masks, yellow_masks)
    masked_img = (cv2.bitwise_and(darkened_img, darkened_img, mask=mask))
    viewImage(masked_img, 'mask')
    blurred_img = gaussian_blur(masked_img, kernel_size=7)
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

lines = linii(img)
print(line)
viewImage(lines, 'kegb')

# cv2.imwrite('line.png',lines)
################################### распознавание линии


# print(yaw("line.png"))
