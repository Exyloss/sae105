import matplotlib.pyplot as pyp
import pandas as p
import json

def get_hour(liste: list) -> list:
    heures = []
    for i in liste:
        heures.append(int(i.split(":")[1:2][0]))
    return heures

f = open('http.json')

data = json.load(f)

f.close()

"""
heure = get_hour(data)

nb_heures = {}

for i in heure:
    nb_heures[i] = nb_heures.get(i, 0)+1

df = p.DataFrame({'heures': nb_heures.keys(), 'Nombre de connections': nb_heures.values()})

df.plot.bar(x='heures', y='Nombre de connections')

"""

dic = {}

for i in data:
    dic[i] = dic.get(i, 0)+1


pyp.figure(figsize=(8,8))

pyp.pie(dic.values(), labels=dic.keys(), normalize=True)

pyp.legend()



pyp.show()
