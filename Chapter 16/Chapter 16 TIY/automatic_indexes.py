from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt

path = Path('Part II\\data_visualization\\Chapter 16\\weather_data\\sitka_weather_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

#Hard coding the indexes for min and max 
date_index = header_row.index('DATE')
high_index = header_row.index('TMAX')
low_index = header_row.index('TMIN')
station_index = header_row.index('STATION')
first_row = next(csv.reader(lines[1:]), None)

dates, highs, lows, stations = [], [], [], []

for row in reader:
    current_date = datetime.strptime(row[date_index],
                                         '%Y-%m-%d')
    if first_row:
        station_name = first_row[station_index]
    else:    
        station_name = 'Unknown'
    try:    
        high = int(row[high_index])
        low = int(row[low_index])
    except ValueError:
        print(f"Missing data for {current_date}")
    else:
        dates.append(current_date)
        highs.append(high)
        lows.append(low)

# Plot the high and low temperatures.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha = 0.5)
ax.plot(dates, lows, color='blue', alpha = 0.5)
ax.fill_between(dates, highs, lows, facecolor = 'blue', alpha = 0.2)

# Format plot.
ax.set_title(f"High and Low Temperatures, 2021 {station_name}", fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()