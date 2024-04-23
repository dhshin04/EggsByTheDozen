import cv2, sys
import numpy as np
from imageHelper import pad, pad_all

from ellipseDetector import ellipseDetector

def getBestEllipse(ellipseHelper, Contour):
    return ellipseHelper.fitEllipse_Polygon(Contour)

def main():
    saveImages = True
    displayImages = True
    
    
    
    fileName = "unlabeled3.jpg"
    thresh = 210
    
    for i in range(0, len(sys.argv)):
        if (sys.argv[i] == "-f"):
            fileName = sys.argv[i+1]
        elif (sys.argv[i] == "-t"):
            thresh = int(sys.argv[i+1])
    
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    binary = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1] 
    
    
    #Otsu Test Can Be Implemented to Guess Threshold Values#
    #im_bw = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    
    
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
    
    cv2.imwrite("imParasites.png", ellipseImage);
    print("Seen: %d" % num_eggs)
    print("Eggs Per Gram: %d" % (num_eggs * 50))
    
    
if __name__=="__main__":
    main()