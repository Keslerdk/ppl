import urllib.request as urllib2
import numpy as np
import cv2
import time
def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def get_raw():
    request = urllib2.Request('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
    raw = []
    try:
        arr = np.asarray(bytearray(urllib2.urlopen(request).read()), dtype=np.uint8)
    except:
        time.sleep(0.5)
        raw =get_raw()
    else:
        raw = cv2.imdecode(arr, -1)
    return raw
#img=get_raw()
#cv2.imwrite('vid_s_clevera.png', img)
img = cv2.imread('vid_s_clevera.png')
viewImage(img, 'fd')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
viewImage(blur_gray, 'gli')

low_threshold =50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
viewImage(edges, 'iv')

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
viewImage(line_image, 'hv')

lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
viewImage(lines_edges, 'lhv')