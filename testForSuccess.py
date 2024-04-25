from testHelper import *
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
import matplotlib.pyplot as plt
import matplotlib.lines as mlines





Images = getTestImagePacks()
names = ["Easy", "Medium", "Hard", "Very Hard", "Healthy Control"]

expected_eggs= []
observed_eggs = []

for Image in Images:
    expSeen, expEggGram = getExpectedData(Image)
    observed, error = getSingleTestError(Image, -1)
    obsSeen, obsEggGram = deriveData(observed)
    expected_eggs.append(expEggGram)
    observed_eggs.append(obsEggGram)   
    print(error)
    
    
colors = ['orange' if x > 650 else 'lightcoral' if x > 350 else 'yellow' if x > 50 else 'green' for x in observed_eggs]
expColors = ['orange' if x > 650 else 'lightcoral' if x > 350 else 'yellow' if x > 50 else 'green' for x in expected_eggs]

# Setting up the bar positions
x = np.arange(len(Images))  # the label locations
width = 0.35  # the width of the bars

expected_eggs = [exp for exp in expected_eggs]
observed_eggs = [obs for obs in observed_eggs]

fig, ax = plt.subplots()

thresholds = [(650, 1750, 'lightcoral', 'Heavy'),
              (350, 650, 'orange', 'Moderate'),
              (50, 350, 'yellow', 'Light'),
              (0, 50, 'green', 'Healthy')]

threshold_patches = []
for bottom, top, color, label in thresholds:
    patch = ax.axhspan(bottom, top, facecolor=color, alpha=0.5, label=label)
    threshold_patches.append(patch)

rects1 = ax.bar(x, observed_eggs, width, label='Observed Eggs Per Gram', color='skyblue')

# Plotting the dotted line for expected eggs
for i, val in enumerate(expected_eggs):
    ax.hlines(y=val, xmin=i - width, xmax=i + width, colors='black', linestyles='dotted', label='Expected Eggs Per Gram' if i == 0 else "")
    
threshold_values = [0,50, 350, 650,1650]
threshold_labels = ['0','Healthy (<50)', 'Light Infestation (50-350)', 'Moderate Infestation (350-650)', 'Heavy Infestation (>650)']
#ax.set_yticks(threshold_values)
#ax.set_yticklabels(threshold_labels)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Selected Test Samples (based on complextiy)', labelpad=20)
ax.set_ylabel('Eggs Per Gram')
ax.set_title('Expected vs Observed Parasitic Eggs Per Gram in Selected Ruminant Fecal Samples')
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylim(bottom=-50)  # Setting the y-axis to start at -50



# Function to attach a label above each bar
def autolabel(rects):
    """Attach a label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
#autolabel(rects2)

legend_colors = [mlines.Line2D([], [], color='skyblue', marker='s', linestyle='None', label='Observed Eggs/g'),
                 mlines.Line2D([], [], color='black', linestyle='dotted', lw=2, label='Expected Eggs/g')]
legend_colors.extend(threshold_patches)
ax.legend(handles=legend_colors, loc='upper right')

#handles, labels = ax.get_legend_handles_labels()
#by_label = dict(zip(labels, handles))
#ax.legend(by_label.values(), by_label.keys())

fig.tight_layout()

#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2)

    
plt.show()
    