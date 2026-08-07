from random import randint
import plotly.express as px
import pandas

from die import Die

#Create two D8. 
die_1 = Die(8)
die_2 = Die(8)

#Make and store rolls in a list. 
results = []

for roll_num in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)
    
#Analyze the results.
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result + 1)

for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

#Visualize results
title = "Results of Rolling Two D8 1,000x"
labels = {'x': 'Result', 'y': 'Frequency'}
fig = px.bar(x=poss_results, y=frequencies, title = title, labels = labels)

fig.show()
#fig.write_html("dice_visual_D6_D10.html")