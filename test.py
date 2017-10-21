import numpy as np
import pandas as pd 
import matplotlib.image as mpimg
import cv2, os
from sklearn.model_selection import train_test_split


IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


data_df = pd.read_csv('driving_log.csv', names=['center', 'speed', 'steering'])

X = data_df['center'].values
y = data_df['steering'].values

X_train, X_valid, y_train, y_valid = train_test_split(X,y,test_size = 0.2)


def load_image(data_dir, image_file):
    """
    Load RGB images from a file
    """
    return mpimg.imread(os.path.join(data_dir, image_file.strip()))


def crop(image):
    """
    Crop the image (removing the sky at the top and the car front at the bottom)
    """
    return image[100:-1, :, :] # remove the sky and the car front


def resize(image):
    """
    Resize the image to the input shape used by the network model
    """
    return cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)

def rgb2yuv(image):
    """
    Convert the image from RGB to YUV (This is what the NVIDIA model does)
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2YUV)


for i in range(0,1000):
    center = X[634 + i]
    image = load_image("IMG",center)
    
    
    image = crop(image)
    image = resize(image)
    image = rgb2yuv(image)

    
    cv2.imshow('image',image)
    cv2.waitKey(5)