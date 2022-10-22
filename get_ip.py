import requests
import os
import urllib
import json

f = open("apache.log", "r")
url = "http://ip-api.com/json/"
listip=[]
dic={}
for ligne in f :
    a=ligne.split(" ")[0]
    if a not in listip:
        listip.append(a)

print(len(listip))

"""
for a in listip:
    response = urllib.request.urlopen (url + a)
    data = response.read()
    values = json.loads(data)
    dic[values['city']] = dic.get(values['city'], 0)+1
"""
"""
while True:
    ip=input("Quelle est l'ip cible: ")
    url = "http://ip-api.com/json/"
    response = urllib.request.urlopen (url + ip)
    data = response.read()
    values = json.loads(data)

    print(" IP: " + values['query'])
    print(" City: " + values['city'])
    print(" ISP: " + values['isp'])
    print("Country: " + values['country'])
    print("Region: " + values['region'])
    print("Time zone: " + values['timezone'])

    break
"""
