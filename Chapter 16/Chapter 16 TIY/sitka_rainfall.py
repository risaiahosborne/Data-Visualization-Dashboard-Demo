from pathlib import Path
import csv
from datetime import datetime

import matplotlib.pyplot as plt

path = Path('Part II\\data_visualization\\Chapter 16\\weather_data\\sitka_weather_2021_full.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

#for index, column_header in enumerate(header_row):
    #print(index, column_header)
    
# Extract dates, and high and low temperatures.
dates, rainfall_list = [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    rainfall = int(float(row[5]))
    dates.append(current_date)
    rainfall_list.append(rainfall)

# Plot the high and low temperatures.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, rainfall_list, color='red', alpha = 0.5)

# Format plot.
ax.set_title("Daily Rainfall \nSitka, 2021", fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Rainfall ('inches')", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()