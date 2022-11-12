import matplotlib.pyplot as pyp
import matplotlib.dates as mdates
import json
from export_file import *
import pandas as p

def format_date(tab: list):
    for i in range(len(tab)):
        tab[i] = tab[i].split("[")[-1].split(" ")[0]
    return tab


f = open('infos.json')

data = json.load(f)

f.close()

countries = [i['country'] for i in data]

dic = {}

for i in countries:
    dic[i] = dic.get(i, 0)+1

"""
pyp.figure(figsize=(8,8))

pyp.pie(dic.values(), labels=dic.keys(), normalize=True)

pyp.legend()
"""

df = p.DataFrame({'Pays': dic.keys(), 'Nombre de connections': dic.values()})
df.plot.bar(x='Pays', y='Nombre de connections')

pyp.show()
