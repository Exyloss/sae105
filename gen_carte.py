#!/usr/bin/env python3
import folium
from parse import list_ip, ip_coord

m = folium.Map(location=[50, 0], zoom_start=5)

ip_tab = list_ip("apache.log")

coord = ip_coord(ip_tab, 10)

for ip in coord.keys():
    folium.Marker(coord[ip], popup="<i>"+ip+"</i>").add_to(m)


m.save("index.html")
