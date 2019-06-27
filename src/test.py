import cv2
import numpy as np
#img = cv2.imread("test.png")
img = cv2.imread("../img/test/nocrop.png")
canny = cv2.Canny(img, 50, 200)

## find the non-zero min-max coords of canny
pts = np.argwhere(canny>0)
y1,x1 = pts.min(axis=0)
y2,x2 = pts.max(axis=0)
y1 -= 3
x1 -= 3
y2 += 3
x2 += 3 

## crop the region
img = img[y1:y2, x1:x2]
cv2.imwrite("../img/test/cropped.png", img)

tagged = cv2.rectangle(img.copy(), (x1,y1), (x2,y2), (0,255,0), 2, cv2.LINE_AA)
cv2.imshow("tagged", tagged)
cv2.waitKey()