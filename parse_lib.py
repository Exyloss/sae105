#!/usr/bin/env python3

import re
import requests
import json
from time import sleep
from export_file import *

def parse(file: str, filter_bot: bool = False, uniq: bool = False) -> list:
    lines = open(file, 'r').readlines()
    tab = []
    ip_list = []
    for line in lines:
        ip = line.split(" ")[0]
        if not uniq or ip not in ip_list:
            ip_list.append(ip)
            # Première valeur entre crochets
            date = re.findall(r"\[.*?\]", line)[0]
            # On récupère le premier nombre à trois chiffres de la ligne
            exit_code = re.findall(" [0-9]{3} ", line)[0][1:-1]
            # Dernière valeur entre double quillemets
            browser = get_browser(line)
            try:
                systeme = get_system(re.findall(r"\(.*?\)", line)[0])
            except:
                systeme = "Unknown"
            if filter_bot == False or (browser != "Robot" and "http" not in systeme):
                tab.append({'ip': ip, 'date': date, 'http_code': exit_code, 'system': systeme, 'browser': browser})
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

def get_system(line) -> str:
    try:
        if "Android" in line:
            return "Android "+re.findall(r"Android \d{1,2}", line)[0].split(" ")[1]
        elif "Linux" in line:
            return "Linux"
        elif "Windows" in line:
            return "Windows NT "+re.findall(r"Windows NT .*?;", line)[0].split(" ")[-1].split(";")[0]
        elif "iPhone" in line:
            return "iPhone "+re.findall(r"iPhone OS \d{1,2}", line)[0].split(" ")[-1]
        elif "Macintosh" in line:
            return "Macintosh "+re.findall(r"Mac OS X \d{1,2}", line)[0].split(" ")[-1]
        else:
            return "Unknown"
    except:
        return "Unknown"

def getIP_infos(ip: str) -> dict:
    url = "http://ip-api.com/json/"
    response = requests.get(url+ip)
    data = response.content
    values = json.loads(data)
    return values

"""
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
    exportToCSVFile(coords, "ip.csv")
    return coords
"""

def ip_infos(tab):
    url = "http://ip-api.com/json/"
    values = []
    for i in range(len(tab)):
        ip = tab[i]
        infos = getIP_infos(ip)
        if infos['status'] == 'success':
            values.append({'ip': ip, 'country': infos['country'], 'isp': infos['isp'], 'lat': infos['lat'], 'lon': infos['lon']})
            print(i)
            sleep(1.1)
        else:
            print("erreur")
    exportToJSONFile(values, "infos.json")
    return values

def get_data(liste: list, data: list) -> list:

    tab = []
    for line in liste:
        tab.append({})
        for i in data:
            tab[-1][i] = line[i]
    return tab

def print_tab(liste: list) -> None:
    is_dic = isinstance(liste[0], dict)
    for line in liste:
        if is_dic:
            print("|".join([i for i in line.values()]))
        else:
            print(line)

def browser_stat(browser_list: list) -> dict:
    dic = {"Edge": {}, "Chrome": {}, "Safari": {}, "Firefox": {}, "Opera": {}}
    for i in browser_list:
        if i != "Unknown Browser" and i != "Robot":
            [browser, version] = i.split("/")
            dic[browser]["total"] = dic[browser].get("total", 0)+1
            dic[browser][version] = dic[browser].get(version, 0)+1
    return dic

def system_stat(system_list: list) -> dict:
    dic = {"iPhone": {}, "Android": {}, "Macintosh": {}, "Windows NT": {}, "Linux": {}, "Unknown": {}}
    for i in system_list:
        try:
            if "Android" in i:
                system = "Android"
                version = re.findall("Android \d{1,2}", i)[0].split(" ")[1]
            elif "Linux" in i:
                system = "Linux"
                version = "erreur"
            elif "Windows" in i:
                system = "Windows NT"
                version = re.findall("Windows NT .*?;", i)[0].split(" ")[-1].split(";")[0]
            elif "iPhone" in i:
                system = "iPhone"
                version = re.findall("iPhone OS \d{1,2}", i)[0].split(" ")[-1]
            elif "Macintosh" in i:
                system = "Macintosh"
                version = re.findall("Mac OS X \d{1,2}", i)[0].split(" ")[-1]
            else:
                continue
        except:
            system = "Unknown"
            version = "erreur"

        dic[system]["total"] = dic[system].get("total", 0)+1
        if version != "erreur":
            dic[system][version] = dic[system].get(version, 0)+1

    return dic

if __name__ == "__main__":
    system = "(Windows NT 6.1; Win64; x64)"
    print(get_system(system))
