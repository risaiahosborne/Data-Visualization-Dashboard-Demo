from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt

def get_data(path, dates, highs, lows, date_index, 
             high_index, low_index):
    """Grabs data from the file"""
    lines = path.read_text().splitlines()
    reader = csv.reader(lines)
    header_row = next(reader)
    
    for row in reader:
        current_date = datetime.strptime(row[date_index],
                                         '%Y-%m-%d')
        try:    
            high = int(row[high_index])
            low = int(row[low_index])
        except ValueError:
            print(f"Missing data for {current_date}")
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)    
            
path = Path(
    'Part II\\data_visualization\\Chapter 16\\weather_data\\sitka_weather_2021_simple.csv'
    )
dates, highs, lows = [], [], []
get_data(
    path, dates, highs, lows, date_index = 2, 
             high_index = 4 , low_index = 5
        )

# Plot the high and low temperatures.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha = 0.5)
ax.plot(dates, lows, color='blue', alpha = 0.5)
ax.fill_between(dates, highs, lows, 
                facecolor = 'blue', alpha = 0.2)

path_1 = Path(
    'Part II\\data_visualization\\Chapter 16\\weather_data\\4330846.csv'
            )
dates, highs, lows = [], [], []
get_data(
    path_1, dates, highs, lows, date_index = 2, 
             high_index = 4 , low_index = 5
        )
# Plot the high and low temperatures.
ax.plot(dates, highs, color='green', alpha = 0.5)
ax.plot(dates, lows, color='yellow', alpha = 0.5)
ax.fill_between(dates, highs, lows, 
                facecolor = 'yellow', alpha = 0.2)

# Format plot.
ax.set_title(
    "Daily High and Low Temp. Comparison, 2021\nSitka v. San Fransico",
             fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(labelsize=16)
ax.set_ylim(0, 150)

plt.show()