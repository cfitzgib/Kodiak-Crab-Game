import math
import cv2
import os, sys
from PIL import Image
import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os
from skimage.data import data_dir
from skimage.util import img_as_ubyte
from skimage import io
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
import csv

# calculate the greyscale value of each pixel
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

#Performs the binarization process with a threshold of .4
def binarize_image(original):
    #Binarize the image if not already greyscale
    if(isinstance(original[0][0], np.ndarray)):
        gray = rgb2gray(original)
    else:
        gray = original
    #print(gray)
    height = len(gray)
    width = len(gray[0])
    for row in range(0, height):
        for col in range(0, width):
            if gray[row][col] > .4:
                gray[row][col] = 1 # turn the pixel white
            else:
                gray[row][col] = 0 # turn the pixel black
    return gray

#Performs the morphological filtering operation on a grayscale image
def filter_image(gray):
    #Create a structuring element and filter the image
    selem = disk(25)
    img = closing(img_as_ubyte(gray), selem)

    #Read in the filtered image and label it
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
    img = cv2.bitwise_not(img)
    connectivity = 100
    output = cv2.connectedComponentsWithStats(img, connectivity, cv2.CV_32S)
    #binary_map = (img > 0).astype(np.uint8)
    labels = output[1]

    # Map component labels to hue val
    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 255
    return output, labeled_img

#Takes in the labeled image and what it should be called, saves the labeled
#version and outputs a csv with its xcenter, ycenter, and pixel area
def save_image_and_csv(image_name, labeled_img, stats, centroids):
    #save labeled image
                cv2.imwrite(image_name[:-4] + "_labeled.png", labeled_img)
               
                with open(image_name[:-4] + '_area.csv', 'w', newline='') as csvfile:
                    areawriter = csv.writer(csvfile, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    for i in range(1, len(stats)):
                        areawriter.writerow([np.array2string(stats[i][4]) + "," + np.array2string(centroids[i][0]) + "," + np.array2string(centroids[i][1])] )

if __name__ == '__main__':
    folder = sys.argv[1] #top level of directory where images are
    #go through directory
    for subdir, dirs, files in os.walk(os.path.join(os.getcwd(), folder)):
        for filename in files:
            
            if(filename[-4:] == ".tif"):
                img_name = subdir + '/' + filename

                #Resize the image
                size = 580 , 486
                im = Image.open(img_name)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(img_name[:-4] + "_resized.png")
                original = mpimg.imread(img_name[:-4] + "_resized.png")
                
                #binarize the image
                gray = binarize_image(original)

                #perform morphological filtering
                output, labeled_img = filter_image(gray)
        
                # The third cell is the stat matrix
                stats = output[2]
                # The fourth cell is the centroid matrix
                centroids = output[3]

                save_image_and_csv(img_name, labeled_img, stats, centroids)
                