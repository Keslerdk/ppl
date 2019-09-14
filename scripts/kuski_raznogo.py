'''image = cv2.imread("/home/trinity/Загрузки/line2.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray_image,164,255,cv2.THRESH_BINARY)
#viewImage(image, "lol")
#viewImage(thresh1, "lol2")
viewImage(gray_image,"gray")'''

'''image = cv2.imread('/home/trinity/Загрузки/line2.jpg')
image = cv2.cvtColor(image,cv2.COLOR_BGR2HLS)
viewImage(image, "1")
lower = np.uint8([0, 200, 0])
upper = np.uint8([255, 255, 255])
white_mask = cv2.inRange(image, lower, upper)
viewImage(white_mask, '2') ## 2'''

'''lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)'''
import cv2
def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows

''''#-----Reading the image-----------------------------------------------------
img = cv2.imread('vid_s_clevera.png', 1)
#cv2.imshow("img",img)
viewImage(img, '1')

#-----Converting image to LAB Color model-----------------------------------
lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#cv2.imshow("lab",lab)
#viewImage(lab, '2')

#-----Splitting the LAB image to different channels-------------------------
l, a, b = cv2.split(lab)
#cv2.imshow('l_channel', l)
#cv2.imshow('a_channel', a)
#cv2.imshow('b_channel', b)
#viewImage(l,'l')
#viewImage(a,'a')
#viewImage(b,'b')
#-----Applying CLAHE to L-channel-------------------------------------------
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
cl = clahe.apply(l)
#cv2.imshow('CLAHE output', cl)
#viewImage(cl,'kvn')

#-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
limg = cv2.merge((cl,a,b))
#cv2.imshow('limg', limg)
#viewImage(limg,';jv')

#-----Converting image from LAB Color model to RGB model--------------------
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
#cv2.imshow('final', final)
viewImage(final,';vn')
cv2.imwrite('final.png', final)'''
import numpy as np
import math
frame=cv2.imread('vid_s_clevera.png')
viewImage(frame, 'kgg')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
viewImage(gray, 'iuvdsug')
equ = cv2.equalizeHist(gray)
viewImage(equ, 'jlhv')
video = cv2.cvtColor(equ,cv2.COLOR_GRAY2BGR)
#viewImage(video, 'khhj')
hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
viewImage(hsv, ';iug')
low_white = np.array([0, 0, 170], dtype=np.uint8)  # lower parameter for filtering the image hsv
high_white = np.array([255, 255, 255], dtype=np.uint8)  # Upper parameter for filtering the image hsv

mask = cv2.inRange(hsv, low_white, high_white)
