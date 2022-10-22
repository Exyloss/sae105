#!/usr/bin/env python3

import csv
import re
import urllib
import requests
import json
from time import sleep

def log_parser(file: str) -> list:
    lines = open(file, 'r').readlines()
    tab = [["Adresse IP", "Date", "Code HTTP", "Système d'exploitation"]]
    for line in lines:
        ip = line.split(" ")[0]
        date = re.findall(r"\[.*?\]", line)[0]
        exit_code = re.findall(" [0-9]{3} ", line)[0][1:-1]
        try:
            systeme = re.findall("\(.*?\)", line)[0]
        except:
            systeme = "unknow"
        tab.append([ip, date, exit_code, systeme])
    return tab

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

def parse_browser(file: str):
    tab = log_parser(file)
    browsers = {}
    for line in tab:
        agent = line[-1].split(" ")[-1]
        if "bot" in agent:
            agent = "bot"
        elif "Firefox" in agent:
            agent = "Firefox"
        elif "Google" in agent:
            agent = "Chrome"
        elif "Edg" in agent:
            agent = "Edge"
        elif "Safari" in agent:
            agent = "Safari"
        else:
            agent = "Autre"

        browsers[agent] = browsers.get(agent, 0)+1
    return browsers

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

def exportToCSVFile(liste, fichier):
    try:
        with open(fichier, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for line in liste:
                writer.writerow(line)
        return True
    except:
        return False

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

exportToCSVFile(log_parser("apache.log"), "out.csv")

#print(parse_os())
#print(parse_browser())
#ips = list_ip("apache.log")
#ip_coord(ips, 50)
#print(re_parse_date("apache.log"))
#print(getIP_infos("66.249.66.75"))
#print(re_parse_http('apache.log'))
#exportToCSVFile(log_parser(), "out.csv")
