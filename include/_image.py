import numpy as np
import os
import cv2
import PIL
import _network
from PIL import Image
from matplotlib import pyplot as plt

def crop(img):
    blurred = cv2.blur(img, (3,3))
    canny = cv2.Canny(blurred, 50, 200)

    ## find the non-zero min-max coords of canny
    pts = np.argwhere(canny>0)
    y1,x1 = pts.min(axis=0)
    y2,x2 = pts.max(axis=0)
    y1 -= 3
    x1 -= 3
    y2 += 3
    x2 += 3 

    img = img[y1:y2, x1:x2]
    ## crop the region
    return img

def preprocessing(img,b):

    basewidth = b
    new_path = "../img/tmp/test.png"
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, basewidth), PIL.Image.ANTIALIAS)
    img.save(new_path)

    img = cv2.imread(new_path, 0)
    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    
    new_img = cv2.bitwise_not(img) / 255.0

    #cv2.imshow('image',new_img)
    #cv2.waitKey(0)

    x = np.size(new_img,0)
    y = np.size(new_img,1)

    for i in range (0,x):
        for j in range (0,y):  
            if new_img[i][j] > 0.5 :
                new_img[i][j] = 1
            else :
                new_img[i][j] = -1

    return new_img

def plot(test, predicted, figsize=(5, 6)):
    test = [d for d in test]
    predicted = [d for d in predicted]

    fig, axarr = plt.subplots(len(test), 2, figsize=figsize)
    for i in range(len(test)):
        if i==0:
            axarr[0].set_title("Input data")
            axarr[1].set_title("Output data")

        axarr[0].imshow(test[i])
        axarr[0].axis('off')
        axarr[1].imshow(predicted[i])
        axarr[1].axis('off')

    plt.tight_layout()
    plt.savefig("../img/tmp/result.png")
    plt.plot()
    plt.waitforbuttonpress(1)
    plt.close()

def plotFixed(test, predicted, figsize=(5, 6)):
    test = [d for d in test]
    predicted = [d for d in predicted]

    fig, axarr = plt.subplots(len(test), 2, figsize=figsize)
    for i in range(len(test)):
        if i==0:
            axarr[0].set_title("Input data")
            axarr[1].set_title("Output data")

        axarr[0].imshow(test[i])
        axarr[0].axis('off')
        axarr[1].imshow(predicted[i])
        axarr[1].axis('off')

    plt.tight_layout()
    plt.savefig("../img/tmp/result.png")
    plt.show()

