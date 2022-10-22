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
    tab = [["Adresse IP", "Date", "Code HTTP", "Système d'exploitation", "Navigateur"]]
    for line in lines:
        ip = line.split(" ")[0]
        # Première valeur entre crochets
        date = re.findall(r"\[.*?\]", line)[0]
        # On récupère le premier nombre à trois chiffres de la ligne
        exit_code = re.findall(" [0-9]{3} ", line)[0][1:-1]
        # Dernière valeur entre double quillemets
        #user_agent = re.findall('".*?"', line)[-1]
        browser = str(get_browser(line))#+":"+ap.simple_detect(user_agent)[1]
        try:
            systeme = re.findall("\(.*?\)", line)[0]
        except:
            systeme = "Unknown OS"
        tab.append([ip, date, exit_code, systeme, browser])
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

def re_parse_http(filename: str) -> dict:
    dic = {}
    log = open(filename, 'r').read()
    exit_code = re.findall(" [0-9]{3} ", log)
    for i in exit_code:
        dic[i[1:-1]] = dic.get(i[1:-1], 0)+1
    return dic

def re_parse_date(filename):
    log = open('apache.log', 'r').read()
    date = re.findall(r"\[.*?\]", log)
    return date

def parse_http(file: str):
    tab = log_parser(file)
    dic = {}
    for i in tab:
        dic[i[-4]] = dic.get(i[-4], 0)+1
    return dic

def parse_os(file: str):
    tab = log_parser(file)
    systemes = []
    for line in tab:
        try:
            agent = line[-1]
            systemes.append(re.findall("\(.*?\)", agent)[0])
        except:
            continue
    return systemes

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

def ip_coord(tab, n):
    url = "http://ip-api.com/json/"
    coords = []
    for i in range(n):
        response = urllib.request.urlopen(url + tab[i])
        data = response.read()
        values = json.loads(data)
        coords.append([values['lat'], values['lon']])
        print("i:",i)
        sleep(0.5)
    exportToCSVFile(coords, "ip.csv")
    return coords


"""
url = "http://ip-api.com/json/66.249.66.75"
response = urllib.request.urlopen(url)
data = response.read()
values = json.loads(data)
print(values)
"""

#print(len(list_ip("apache.log")))

#print(get_browser('20.203.142.208 - - [09/Nov/2021:12:05:51 +0100] "GET /en/index.php?controller=\"><script%20>alert(String.fromCharCode(88,83,83))</script> HTTP/1.1" 301 4932 "https://controltower.fr/en/index.php?controller=\"><script >alert(String.fromCharCode(88,83,83))</script>" "Mozilla/5.0 (Windows NT 10.0; WOW64; Rv:50.0) Gecko/20100101 Firefox/50.0"'))

exportToCSVFile(log_parser("apache.log"), "out.csv")

#print(parse_os())
#print(parse_browser())
#ips = list_ip("apache.log")
#ip_coord(ips, 50)
#print(re_parse_date("apache.log"))
#print(getIP_infos("66.249.66.75"))
#print(re_parse_http('apache.log'))
#exportToCSVFile(log_parser(), "out.csv")
