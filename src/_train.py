import sys
import pickle
sys.path.append('../include')

import numpy as np
import os
import _network
from _utils import verify
from _image import preprocessing, plotFixed, plot
from PIL import Image

SIZE = 28

# Main

def main():

    # Load data
    f_square = os.path.join('../img/data/newsquare.png')
    square = Image.open(f_square)
    f_triangle1 = os.path.join('../img/data/newtriangle1.png')
    triangle1 = Image.open(f_triangle1)
    f_triangle2 = os.path.join('../img/data/newtriangle2.png')
    triangle2 = Image.open(f_triangle2)
    f_triangle3 = os.path.join('../img/data/newtriangle3.png')
    triangle3 = Image.open(f_triangle3)
    f_triangle4 = os.path.join('../img/data/triangle4.png')
    triangle4 = Image.open(f_triangle4)
    f_triangle5 = os.path.join('../img/data/triangle5.png')
    triangle5 = Image.open(f_triangle5)
    f_triangle6 = os.path.join('../img/data/triangle6.png')
    triangle6 = Image.open(f_triangle6)
    f_triangle7 = os.path.join('../img/data/triangle7.png')
    triangle7 = Image.open(f_triangle7)
    f_triangle8 = os.path.join('../img/data/triangle8.png')
    triangle8 = Image.open(f_triangle8)
    f_circle = os.path.join('../img/data/newcircle.png')
    circle = Image.open(f_circle)
    f_blank = os.path.join('../img/data/blank.png')
    blank = Image.open(f_blank)

    # Merge data
    data = [square, triangle1, triangle2, triangle3, circle]

    # Preprocessing
    print("Start to data preprocessing...")
    data  = [preprocessing(d,SIZE) for d in data]

    # Create Hopfield Network Model
    model = _network.HopfieldNetwork()

    # Calculate Weights
    model.train_weights(data)
    model.plot_weights()

# Execution
if __name__ == '__main__':
    main()
