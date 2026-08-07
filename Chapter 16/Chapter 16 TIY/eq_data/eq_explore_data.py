from pathlib import Path
import json

import plotly.express as px

#Read data as a string and convert to a Python object. 
path = Path('Part II\\data_visualization\\Chapter 16\\Chapter 16 TIY\\eq_data\\eq_data_30_day_m1.geojson')
contents = path.read_text(encoding= 'utf-8')
all_eq_data = json.loads(contents)

#Create a more readable version of the data table.
path = Path('Part II\\data_visualization\\Chapter 16\\Chapter 16 TIY\\eq_data\\readable_eq_data_30_day.geojson') 
readable_contents = json.dumps(all_eq_data, indent = 4)
path.write_text(readable_contents)

#Exmaine all earthquakes in the dataset.
all_eq_dicts = all_eq_data['features']
#print(len(all_eq_dicts))

mags, lons, lats,  eq_titles = [], [], [], []

for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]
    eq_title = eq_dict['properties']['title']
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)
    eq_titles.append(eq_title)

title = 'Global Earthquakes'
fig = px.scatter_geo(
    lat = lats, lon = lons, title = title,
    size = mags, color = mags, color_continuous_scale = 'Viridis',
    labels = {'color': 'Magnitude'}, projection = 'natural earth',
    hover_name = eq_titles, 
    )

fig.show()
#print(mags[:10])
#print(lons[:5])
#print(lats[:5])