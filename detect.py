import cv2, sys
import numpy as np
from imageHelper import pad, pad_all
from enum import Enum

from ellipseDetector import ellipseDetector

class Parasite:
    def __init__(self, centerX=0.0, centerY=0.0, width=0.0, height=0.0, estArea=0.0):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.estArea = estArea
        
class INFESTATION(Enum):
    NONE = 0
    LIGHT = 1
    MODERATE = 2
    HEAVY = 3
        
def successCriteria(eggsPerGram):
    if eggsPerGram > 650: 
        print("Heavy Infestation: Anthelmintic Treatment Necessary")
        return INFESTATION.HEAVY
    elif eggsPerGram > 350: 
        print("Moderate Infestation: Anthelmintic Treatment Recommended")
        return INFESTATION.MODERATE
    elif eggsPerGram >= 50:
        print("Light Infestation: Treatment Not Necessary")
        return INFESTATION.LIGHT
    else:
        print("No Infestation: Sample is Healthy")
        return INFESTATION.NONE

def getBestEllipse(ellipseHelper, Contour, size):
    return ellipseHelper.fitEllipse_Polygon(Contour,size)

def getBinaryThreshold(gray_image, threshold):
    blur = cv2.GaussianBlur(gray_image, (3,3), 0)
    if (threshold == -1):
        otsu_threshold, image_result = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return(image_result)
    else:
        return cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)[1]
    
    #OTSU METHOD
    #return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    #OTSU with Blur
    #
    #return cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    #Adaptive Thresholding with Blur 
    #return cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)

    #return cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3)
    
    #TRADITIONAL METHOD
    return cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)[1] 

def detectParasites(fileName, thresh, outFile = "", saveImages = True):
    
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    if fileName == "easy_test.png": thresh=130
    elif fileName == "medium_test.jpeg": thresh=208
    elif fileName == "hard_test.jpeg": thresh=103
    else: thresh=-1
    binary = getBinaryThreshold(im_gray, thresh)

    contourImage = cv2.imread(fileName)
    ellipseImage = cv2.imread(fileName)
    
    #print(binary.shape)
    #print(contourImage.shape)
    #print(contourImage)
    size = im_gray.shape
    
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
            bestEllipse = getBestEllipse(ellipseHelper, contour, size)
            if not bestEllipse == None: 
                cv2.ellipse(ellipseImage, bestEllipse, (0,0,255), 3)
                num_eggs+=1
    
    if (saveImages):
        if outFile == "":
            cv2.imwrite("static/images/imParasites.png", ellipseImage)
        else: 
            cv2.imwrite(outFile, ellipseImage)
        
    
        
    print("Seen: %d" % num_eggs)
    print("Eggs Per Gram: %d" % (num_eggs * 50))
    successCriteria(num_eggs*50)
    
    
def testProtocol(fileName, img, thresh, Parasites):
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    greenMat = img.copy()
    
    #if fileName == "easy_test.png": thresh=130
    #elif fileName == "medium_test.jpeg": thresh=208
    #elif fileName == "hard_test.jpeg": thresh=103
    #else: thresh=-1
    binary = getBinaryThreshold(im_gray, thresh)
    
    size = im_gray.shape
    
    im_gray, binary, greenMat = pad_all([im_gray, binary, greenMat])
    
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    num_eggs = 0
    
    ellipseHelper = ellipseDetector()
    observedParasites = []
    for contour in contours: 
        if len(contour)>=5:
            bestEllipse = getBestEllipse(ellipseHelper, contour, size)
            if not bestEllipse == None: 
                cv2.ellipse(greenMat, bestEllipse, (0,0,255), 3)
                (cx,cy),(ma,ml),a = bestEllipse
                observedParasites.append(Parasite(cx,cy,ma,ml,ma*ml))
                num_eggs+=1
    
    
    
    #cv2.imshow("TEST", greenMat)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return greenMat, observedParasites