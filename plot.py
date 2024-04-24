import matplotlib.pyplot as plt
import numpy as np

# Data
samples = ['Easy', 'Medium', 'Hard']

errors_image1 = [85,75, 90, 75,75,]
errors_image2 = [556,525,506, 546,545,]
errors_image3 = [486,496, 493, 467,482,]



# Calculating total sales for 2021 by summing car sales and real-estate sales
observed_parasites = [car + real_estate for car, real_estate in zip(correct_parasites, false_positives)]

# X locations for the groups
x = np.arange(3)

# Width of the bars
width = 0.35

# Creating the bar graph
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, expected_parasites, width, label='Expected')
rects2 = ax.bar(x + width/2, false_positives, width, label='False Positives', bottom=correct_parasites)
ax.bar(x + width/2, correct_parasites, width, label='Correctly Identified Parasites', color='green')

# Adding labels, title, and custom x-axis tick labels
ax.set_xlabel('Month')
ax.set_ylabel('Sales (in units)')
ax.set_title('Monthly Sales Comparison between 2020 and 2021')
ax.set_xticks(x)
ax.set_xticklabels(samples)
ax.legend()

# Function to attach a text label above each bar in *rects*
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Call the function for each set of bars
autolabel(rects1)
autolabel(rects2)

# Show the plot
plt.show()
