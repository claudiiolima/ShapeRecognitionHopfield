# -*- coding: utf-8 -*-

import sys
import pickle
sys.path.append('../include')

import numpy as np
import os
import _network
from _utils import verify, compare
from _image import preprocessing, plotFixed, plot, crop
from PIL import Image

SIZE = 28

def predict():
    # Load reference data
    f_square = os.path.join('../img/data/newsquare.png')
    square = Image.open(f_square)
    f_triangle1 = os.path.join('../img/data/newtriangle1.png')
    triangle1 = Image.open(f_triangle1)
    f_triangle2 = os.path.join('../img/data/newtriangle2.png')
    triangle2 = Image.open(f_triangle2)
    f_triangle3 = os.path.join('../img/data/newtriangle3.png')
    triangle3 = Image.open(f_triangle3)
    f_circle = os.path.join('../img/data/newcircle.png')
    circle = Image.open(f_circle)
    f_blank = os.path.join('../img/data/blank.png')
    blank = Image.open(f_blank)

    # Merge and Preprocessing reference data
    data = [square, triangle1, triangle2, triangle3, circle]
    data = [preprocessing(d,SIZE) for d in data]

    # Load data
    f_image = os.path.join('../img/tmp/tmp.png')
    t_image = Image.open(f_image)

    # Merge data
    test = [t_image]

    # Preprocessing
    ## print("Start to data preprocessing...")
    test = [preprocessing(t,SIZE) for t in test]

    # Create Hopfield Network Model
    model = _network.HopfieldNetwork()

    # Load Weights  
    model.load_weights()

    # Save the model predicted
    predicted = model.predict(test, SIZE, threshold=800, asyn=False)

    i = 0
    temp = []
    test_new = []
    _bool = True
    
    _verify = verify(data,predicted)
    temp.append(predicted[0])

    _threshold = 800

    while (not _verify) & (_threshold > 40):
        del predicted[:]
        predicted = model.predict(test, SIZE, threshold=_threshold, asyn=False)
        _verify = verify(data,predicted)
        _threshold -= 5
        #plot(test,predicted)
        if not np.allclose(temp[i],predicted):
            i += 1
            temp.append(predicted[0])
    
    temp = [d for d in temp]
    
    for k in range(len(temp)-1,-1,-1):
        _threshold = 800
        while (not _verify) & (_threshold > 40):
            del test_new[:]
            del predicted[:]
            test_new.append(temp[k])
            predicted = model.predict(test_new, SIZE, threshold=_threshold, asyn=False)
            _verify = verify(data,predicted)
            _threshold -= 15
            #plot(test_new,predicted)
    #plotFixed(test,predicted)

    return compare(data,predicted)
        
    #print("Show network weights matrix...")
    #model.plot_weights()

# Main
def main():
    predict();
    

# Execution
if __name__ == '__main__':
    main()