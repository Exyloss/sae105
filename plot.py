import matplotlib.pyplot as pyp
import json

f = open('browser.json')

data = json.load(f)

f.close()

keys = []
values = []

for i in data.keys():
    keys.append(i)
    values.append(data[i]["total"])

pyp.figure(figsize=(8,8))

pyp.pie(values, labels=keys, normalize=True)

pyp.legend()

pyp.show()
