#!/usr/bin/env python3

import csv
import re
import urllib
import requests
import json
from time import sleep
import httpagentparser as ap
from export_file import *

def log_parser(file: str) -> list:
    lines = open(file, 'r').readlines()
    # Nom des colonnes pour exporter le tableau
    tab = []
    for line in lines:
        ip = line.split(" ")[0]
        # Première valeur entre crochets
        date = re.findall(r"\[.*?\]", line)[0]
        # On récupère le premier nombre à trois chiffres de la ligne
        exit_code = re.findall(" [0-9]{3} ", line)[0][1:-1]
        # Dernière valeur entre double quillemets
        browser = get_browser(line)
        try:
            systeme = re.findall("\(.*?\)", line)[0]
        except:
            systeme = "Unknown OS"
        tab.append({"ip": ip, "date": date, "http": exit_code, "system": systeme, "browser": browser})
    return tab

def get_browser(line):
    user_agent = re.findall('".*?"', line)[-1]
    # ~~ Les joies de Python ~~ #
    if "bot" in user_agent:
        return "Robot"
    elif "Edge/" in user_agent:
        browser = "Edge"
    elif "Firefox/" in user_agent:
        browser = "Firefox"
    elif "Chrome/" in user_agent:
        browser = "Chrome"
    elif "Safari/" in user_agent:
        browser = "Safari"
    elif "Opera/" in user_agent:
        browser = "Opera"
    else:
        return "Unknown Browser"
    return re.findall(browser+'\/.*?(?:"| )', user_agent)[0][:-1]

def getIP_infos(ip):
    url = "http://ip-api.com/json/"
    response = urllib.request.urlopen(url + ip)
    data = response.read()
    values = json.loads(data)
    return {
        "ip": values['query'],
        "city": values['city'],
        "isp": values['isp'],
        "country": values['country'],
        "region": values['region'],
        "timezone": values['timezone']}

def list_ip(file):
    listip = []
    f = open(file, "r")
    for ligne in f :
        a=ligne.split(" ")[0]
        if a not in listip:
            listip.append(a)
    return listip

def ip_coord(tab, a, b):
    url = "http://ip-api.com/json/"
    coords = []
    for i in range(a, b):
        ip = tab[i]
        response = urllib.request.urlopen(url + ip)
        data = response.read()
        values = json.loads(data)
        print(i)
        coords.append([ip, values['lat'], values['lon']])
        sleep(1.5)
    exportToCSVFile(coords, "ip.csv", "a")
    return coords


"""
url = "http://ip-api.com/json/66.249.66.75"
response = urllib.request.urlopen(url)
data = response.read()
values = json.loads(data)
print(values)
"""

#print(len(list_ip("apache.log")))

#exportToCSVFile(log_parser("apache.log"), "out.csv", "w")
#exportToJSONFile(log_parser("apache.log"), "out.json")

#ip_coord(list_ip("apache.log"), 300, 400)

#print(parse_os())
#print(parse_browser())
#ips = list_ip("apache.log")
#ip_coord(ips, 50)
#print(re_parse_date("apache.log"))
#print(getIP_infos("66.249.66.75"))
#print(re_parse_http('apache.log'))
#exportToCSVFile(log_parser(), "out.csv")
