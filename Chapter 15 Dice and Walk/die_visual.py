import plotly.express as px

from die import Die

#Create a D6 and a D10. 
die_1 = Die()
die_2 = Die(10)

#Make and store rolls in a list. 
results = []

for roll_num in range(50_000):
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
title = "Results of Rolling Two D6 and a D10 50,000x"
labels = {'x': 'Result', 'y': 'Frequency'}
fig = px.bar(x=poss_results, y=frequencies, title = title, labels = labels)

fig.update_layout(xaxis_dtick =1)

fig.show()
#fig.write_html("dice_visual_D6_D10.html")