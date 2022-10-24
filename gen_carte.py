#!/usr/bin/env python3
import folium
#from parse import list_ip, ip_coord

m = folium.Map(location=[50, 0], zoom_start=5)

#ip_tab = list_ip("apache.log")

#coord = ip_coord(ip_tab, 10)
coord = []

import csv
with open('ip.csv', mode ='r') as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
      coord.append(lines)
      print(lines)

for ip in coord:
    folium.Marker((ip[1], ip[2]), popup="<i>"+ip[0]+"</i>").add_to(m)


m.save("index.html")
