#!/usr/bin/env python3

from os.path import exists
from parse_lib import *
from export_file import *
import argparse

parser = argparse.ArgumentParser(prog="main.py")

parser.add_argument('log_file')
parser.add_argument('-o', '--output', help="fichier de sortie")
parser.add_argument('-t', '--type', help="type de données du fichier de sortie, valeurs possibles: json, csv, xml")
parser.add_argument('-g', '--get', help="Obtenir une certaine entrée, valeurs possibles: ip, date, http_code, browser, system")
parser.add_argument('-f', '--filter', help="Filtrer les robots", action='store_true')
parser.add_argument('-u', '--uniq', help="Faire que chaque adresse IP soit unique", action='store_true')

args = parser.parse_args()

if not exists(args.log_file):
    print("Erreur, le fichier "+args.log_file+" n'existe pas.")
    exit(1)

if args.output != None and exists(args.output):
    r = input("Attention, le fichier "+args.output+" existe déjà, êtes-vous sûr de vouloir le réécrire (o/n) ? ")
    if r != "o":
        print("Commande annulée.")
        exit(1)

if args.output != None and args.type not in ["csv", "json", "xml"]:
    print("Erreur, le type de fichier "+str(args.type)+" n'existe pas.")
    exit(1)


values = parse(args.log_file, args.filter, args.uniq)

if args.get != None:
    get_args = [i for i in args.get.split(",")]

    for arg in get_args:
        if arg not in ["ip", "date", "http_code", "browser", "system"] and arg != None:
            print("Erreur, la valeur "+args.get+" n'existe pas.")
            exit(1)
    values_get = get_data(values, get_args)
else:
    values_get = values

if args.output == None:
    print_tab(values_get)
else:
    if args.type == "json":
        exportToJSONFile(values_get, args.output)
    elif args.type == "csv":
        exportToCSVFile(values_get, args.output)
    else:
        exportToXMLFile(values_get, args.output)
