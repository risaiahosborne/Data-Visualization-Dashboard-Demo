import numpy as np
import matplotlib.pyplot as plt

from dice import Dice

# Create a D6
die_1 = Dice()

die_1.roll()

#Results
results = die_1.get_results()

x_values = list(range(1, die_1.num_sides + 1))
frequencies = [results.count(value) for value in x_values]
#Graph


plt.bar(x_values, frequencies)

plt.title("Results of 200 rolls")
plt.xlabel("Sides")
plt.ylabel("Frequency")

plt.show()