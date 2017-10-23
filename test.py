import numpy as np
import pandas as pd 
import matplotlib.image as mpimg
import cv2, os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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
    return image[125:-10, 20:-20, :] # remove the sky and the car front


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

def preprocess(image, mtx, dist):
    """
    Combine all preprocess functions into one
    """
#    image = crop(image)
    image = birds_eye(image, mtx, dist)
    image = resize(image)
    image = rgb2yuv(image)
    return image


def load_config():
    with np.load('cam.npz') as calibData:
        mtx, dist = [calibData[i] for i in ('mtx', 'dist')]
    return mtx,dist

# Remove distortion from images
def undistort(image, mtx, dist, show=True, read = True):
    
#    img = cv2.imread(image)
    img = image
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    return undist
        
# Perform perspective transform
def birds_eye(img, mtx, dist):

    undist = undistort(img, mtx, dist, show = False)
    img_size = (undist.shape[1], undist.shape[0])
    
    src = np.float32([[0, 140],[320, 140],
                      [320, 240],[0, 240]])
    dst = np.float32([[0, 0], [320, 0], 
                     [320, 240],[0, 240]])
    
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(undist, M, img_size)
    return warped


mtx,dist = load_config()    


for i in range(0,500):
    center = X[i]
    image = load_image("IMG",center)
    
    #image = preprocess(image, mtx, dist)
    
    bird_image = birds_eye(image,mtx,dist)
    cv2.imshow('image',bird_image)
    cv2.waitKey(5)


#f, (ax1, ax2) = plt.subplots(1, 2, figsize=(9,5))
#ax1.imshow(image)
#ax1.set_title('Original Image', fontsize=20)
#ax2.imshow(bird_image)
#ax2.set_title('Undistorted birds eye view', fontsize=20)



#image = crop(image)


