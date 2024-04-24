import cv2
from testHelper import getTestImagePacks, getTestImages, getTestErrors, getSingleTestError, getSingleTestImage
import matplotlib.pyplot as plt
import numpy as np
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

def optimize(ImagePack):
    ThresVals = []
    TotalError = []
    UndetectedParasites = []
    print(type(ImagePack))
    
    Lowest_Error = (999,0)
    Least_Undetected = (999,0)
    
    for i in range(70, 245, 3):
        undetected,errorVal = getSingleTestError(ImagePack,i)
        ThresVals.append(i)
        TotalError.append(errorVal)
        UndetectedParasites.append(undetected)
        print(errorVal, undetected)
        
        if undetected < Least_Undetected[0]: Least_Undetected = (undetected, i)
        if errorVal < Lowest_Error[0]: Lowest_Error = (errorVal, i)
    
    print(Lowest_Error)
    print(Least_Undetected)
    
    
    return TotalError, UndetectedParasites, Lowest_Error, Least_Undetected
    
    plt.figure(figsize=(10, 6))
    plt.plot(ThresVals, TotalError, label='Total Error', marker='o')
    plt.plot(ThresVals, UndetectedParasites, label='Undetected Parasites', marker='s')
    plt.xlabel('Threshold Values')
    plt.ylabel('Count')
    plt.title('Error Analysis by Threshold')
    plt.legend()
    plt.grid(True)
    plt.show() 
    

def getDataForOptimizeAll(ImagePacks):
    ThresVals = range(70,245,3)
    TotalError1 = []
    TotalError2 = []
    TotalError3 = []
    Undetected1 = []
    Undetected2 = []
    Undetected3 = []
    
    TotalError1, Undetected1, _, _ = optimize(ImagePacks[0])
    TotalError2, Undetected2, _, _ = optimize(ImagePacks[1])
    TotalError3, Undetected3, _, _= optimize(ImagePacks[2])
    
    
    
    plt.figure(figsize=(10, 6))
    plt.plot(ThresVals, TotalError1, label='Error (Easy Img)', marker='o',color='orange')
    plt.plot(ThresVals, TotalError2, label='Error (Medium Img)', marker = '^', color='magenta')
    plt.plot(ThresVals, TotalError3, label='Error (Hard Img)', marker = 'D', color='cyan')
    plt.plot(ThresVals, Undetected1, label='Undetected (Easy)', marker='s', color='orange')
    plt.plot(ThresVals, Undetected2, label = 'Undetected (Med)', marker = 'p', color = 'magenta')
    plt.plot(ThresVals, Undetected3, label='Undetected (Hard)', marker = '*', color='cyan')
    plt.xlabel('Threshold Values')
    plt.ylabel('Count')
    plt.title('Error Analysis by Threshold')
    plt.legend()
    plt.grid(True)
    plt.show() 
    

def optimalDisplay():
    ImageFiles = ["letter2.png", "unlabeled3.jpeg", "arrows1.jpeg"]
    Images = getTestImagePacks()

    
    testImgs = []
    totalErrors = []
    allUndetected = []
    root = tk.Tk()
    
    for Image in Images: 
        totalError, undetected, lowest_error, least_undetected = optimize(Image)
        thresh = least_undetected[1]
        currTestImg = getSingleTestImage(Image, thresh)[0]
        testImgs.append(currTestImg)
        
        totalErrors.append(totalError)
        allUndetected.append(undetected)
        
    ThresVals = range(70,245,3)

    root.title("Optimized Parasite Detection Model")

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    ax.plot(ThresVals, totalErrors[0], label='Error (Easy Img)', marker='o',color='orange')
    ax.plot(ThresVals, totalErrors[1], label='Error (Medium Img)', marker = '^', color='magenta')
    ax.plot(ThresVals, totalErrors[2], label='Error (Hard Img)', marker = 'D', color='cyan')
    ax.plot(ThresVals, allUndetected[0], label='Undetected (Easy)', marker='s', color='orange')
    ax.plot(ThresVals, allUndetected[1], label = 'Undetected (Med)', marker = 'p', color = 'magenta')
    ax.plot(ThresVals, allUndetected[2], label='Undetected (Hard)', marker = '*', color='cyan')
    ax.set_xlabel('Threshold Values')
    ax.set_ylabel('Count')
    ax.set_title('Error Analysis by Threshold')
    ax.grid(True)
    ax.legend()

    label1 = tk.Label(root, image = testImgs[0])
    label2 = tk.Label(root, image = testImgs[1])
    label3 = tk.Label(root, image = testImgs[2])
    
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(row=0, column=1)
    
    


    label1.grid(row=0, column=0)
    label2.grid(row=1, column=0)
    label3.grid(row=1, column=1)

    root.geometry("1500x800")

    root.mainloop()
 
    
    
#imagePacks = getTestImagePacks()
#print(type(imagePacks))
#optimize(imagePacks[2])
#getDataForOptimizeAll(imagePacks)
optimalDisplay()