#!/usr/bin/env python3

import re
import requests
import json
from time import sleep
from export_file import *

def parse(file: str, filter_bot: bool = False) -> list:
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
        if filter_bot == False or browser != "Robot":
            tab.append([ip, date, exit_code, systeme, browser])
    return tab

def get_browser(line) -> str:
    user_agent = re.findall('".*?"', line)[-1]
    # ~~ Les joies de Python ~~ #
    if "bot" in user_agent or "Bot" in user_agent:
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
    response = requests.get(url+ip)
    data = response.content
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
            coords.append((infos['lat'], infos['lon']))
            print(i)
            sleep(1.5)
        else:
            print("erreur")
    exportToCSVFile(coords, "ip.csv", "a")
    return coords

def count_browser(fichier: str):
    values = parse(fichier)
    dic = {}
    for line in values:
        browser = line[-1].split("/")[0]
        dic[browser] = dic.get(browser, 0)+1
    return dic

def count_os(fichier: str):
    values = parse(fichier)
    dic = {}
    for line in values:
        print(line[-2])


def get_data(liste: list, data: str) -> list:
    data_dic = {"ip": 0, "date": 1, "http_code": 2, "browser": 4, "system": 3}
    index = data_dic[data]
    tab = []
    for line in liste:
        tab.append(line[index])
    return tab

def print_tab(liste: list) -> None:
    is_tab = isinstance(liste[0], list)
    for line in liste:
        if is_tab:
            print(" ".join(line))
        else:
            print(line)
