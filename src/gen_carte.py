#!/usr/bin/env python3
import folium
import csv

m = folium.Map(location=[50, 0], zoom_start=5)

coord = []

with open('coord.csv', mode ='r') as file:
  csvFile = csv.reader(file)
  for line in csvFile:
      if line not in coord:
        coord.append(line)

for ip in coord:
    folium.Marker((ip[0], ip[1])).add_to(m)


m.save("index.html")
