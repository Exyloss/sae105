#!/usr/bin/env python3
import folium
import csv

m = folium.Map(location=[50, 0], zoom_start=5)

coord = []

with open('ip.csv', mode ='r') as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
      coord.append(lines)

for ip in coord:
    folium.Marker((ip[1], ip[2]), popup="<i>"+ip[0]+"</i>").add_to(m)


m.save("index.html")
