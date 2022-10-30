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
parser.add_argument('-u', '--uniq', help="Faire que chaque valeur soit unique", action='store_true')

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
    print("Erreur, le type de fichier "+args.type+" n'existe pas.")
    exit(1)

if args.get not in ["ip", "date", "http_code", "browser", "system"] and args.get != None:
    print("Erreur, la valeur "+args.get+" n'existe pas.")
    exit(1)

values = parse(args.log_file, args.filter)

if args.get != None:
    values_get = get_data(values, args.get)
else:
    values_get = values

print_tab(values_get)
