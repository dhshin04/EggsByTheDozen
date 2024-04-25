import cv2, sys
import numpy as np
from imageHelper import pad, pad_all
from detect import detectParasites

def main():
    fileName = "unlabeled3.jpg"
    thresh = 210
    outFile = ""
    
    for i in range(0, len(sys.argv)):
        if (sys.argv[i] == "-f"):
            fileName = sys.argv[i+1]
        elif (sys.argv[i] == "-t"):
            thresh = int(sys.argv[i+1])
        elif (sys.argv[i] == "-o"):
            outFile = sys.argv[i+1]
            
    detectParasites(fileName, thresh, outFile, True)
    
      
if __name__=="__main__":
    main()