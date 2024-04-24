import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import cv2
from matplotlib.animation import FuncAnimation
import sys
from imageHelper import pad, pad_all
from detect import testProtocol, Parasite
import math

from ellipseDetector import ellipseDetector

from testHelper import getTestImages, calculate_error, getTestImagePacks


thresh = 210
ImageFiles = ["easy_test.png", "medium_test.jpeg", "hard_test.jpeg"]
Images = getTestImagePacks()



root = tk.Tk()
testImgs = getTestImages(Images, thresh)[0]
root.title("Image Grid")


label1 = tk.Label(root, image = testImgs[0])
label2 = tk.Label(root, image = testImgs[1])
label3 = tk.Label(root, image = testImgs[2])


label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=1, column=1)

root.geometry("1500x800")

root.mainloop()



    

    
"""
def getBestEllipse(ellipseHelper, Contour):
    return ellipseHelper.fitEllipse_Polygon(Contour)

def getBinaryThreshold(gray_image, threshold):
    #OTSU METHOD
    return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    #TRADITIONAL METHOD
    #return cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)[1] 

def testParasites(fileName, thresh, outFile = "", saveImages = True):
    
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    binary = getBinaryThreshold(im_gray, thresh)

    contourImage = cv2.imread(fileName)
    ellipseImage = cv2.imread(fileName)
    
    #print(binary.shape)
    #print(contourImage.shape)
    #print(contourImage)
    
    im_gray, binary, contourImage, ellipseImage = pad_all([im_gray, binary, contourImage, ellipseImage])
    
    if (saveImages): cv2.imwrite("imThresh.png", binary)
    
    #print(binary)
    #print(binary.shape, contourImage.shape)
    
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    #Filter Contour Areas
    
    cv2.drawContours(contourImage, contours, -1, (0,0,0), 3)
    if (saveImages): cv2.imwrite("imContours.png", contourImage);
    
    #print("savedContours");
    #print(len(contours));
    
    num_eggs = 0
    
    ellipseHelper = ellipseDetector()
    for contour in contours: 
        if len(contour)>=5:
            bestEllipse = getBestEllipse(ellipseHelper, contour)
            if not bestEllipse == None: 
                
                cv2.ellipse(ellipseImage, bestEllipse, (0,0,255), 3)
                num_eggs+=1
    
    if (saveImages):
        if outFile == "":
            cv2.imwrite("imParasites.png", ellipseImage);
        else: 
            cv2.imwrite(outFile, ellipseImage);
        
    
      
    print("Seen: %d" % num_eggs)
    print("Eggs Per Gram: %d" % (num_eggs * 50))"""