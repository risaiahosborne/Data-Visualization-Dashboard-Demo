from random import randint
import plotly.express as px
import pandas

from die import Die

#Create two D8. 
die_1 = Die(6)
die_2 = Die(6)

#Make and store rolls in a list. 
results = [die_1.roll() * die_2.roll() for roll_num in range(1000)]
    
#Analyze the results.
max_result = die_1.num_sides * die_2.num_sides
poss_results = range(1, max_result + 1)
frequencies = [results.count(value) for value in poss_results]

#Visualize results
title = "Results of Rolling Two D6 1,000x and Multiplying"
labels = {'x': 'Result', 'y': 'Frequency'}
fig = px.bar(x=poss_results, y=frequencies, title = title, labels = labels)

fig.show()
#fig.write_html("dice_visual_D6_D10.html")