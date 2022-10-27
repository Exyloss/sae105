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
        tab.append([ip,date, exit_code, systeme, browser])
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

def getIP_infos(ip: str) -> dict:
    url = "http://ip-api.com/json/"
    response = urllib.request.urlopen(url + ip)
    data = response.read()
    values = json.loads(data)
    return values

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
        infos = getIP_infos(ip)
        if infos['status'] == 'success':
            coords.append((ip, infos['lat'], infos['lon']))
            print(i)
            sleep(1.5)
        else:
            print("erreur")
    exportToCSVFile(coords, "ip.csv", "a")
    return coords


#print(len(list_ip("apache.log")))

#exportToCSVFile(log_parser("apache.log"), "out.csv", "w")
exportToJSONFile(log_parser("apache.log"), "out.json")

#ip = list_ip("apache.log")
#exportToText(ip, "list_ip.txt")
#ip_coord(ip, 4000, len(ip))

#print(parse_os())
#print(parse_browser())
#ips = list_ip("apache.log")
#ip_coord(ips, 50)
#print(re_parse_date("apache.log"))
#print(getIP_infos("66.249.66.75"))
#print(re_parse_http('apache.log'))
#exportToCSVFile(log_parser(), "out.csv")
