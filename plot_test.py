import matplotlib.pyplot as plt
import numpy as np

# Data
months = ['January', 'February', 'March', 'April', 'May']
sales_2020 = [200, 220, 250, 210, 230]
car_sales_2021 = [120, 140, 160, 130, 150]  # New data for car sales in 2021
real_estate_sales_2021 = [90, 100, 100, 90, 100]  # New data for real-estate sales in 2021

# Calculating total sales for 2021 by summing car sales and real-estate sales
sales_2021 = [car + real_estate for car, real_estate in zip(car_sales_2021, real_estate_sales_2021)]

# X locations for the groups
x = np.arange(len(months))

# Width of the bars
width = 0.35

# Creating the bar graph
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, sales_2020, width, label='2020')
rects2 = ax.bar(x + width/2, car_sales_2021, width, label='Car Sales 2021', bottom=real_estate_sales_2021)
ax.bar(x + width/2, real_estate_sales_2021, width, label='Real Estate Sales 2021', color='grey')

# Adding labels, title, and custom x-axis tick labels
ax.set_xlabel('Month')
ax.set_ylabel('Sales (in units)')
ax.set_title('Monthly Sales Comparison between 2020 and 2021')
ax.set_xticks(x)
ax.set_xticklabels(months)
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
