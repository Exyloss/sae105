import json
import csv

def exportToCSVFile(liste: list, fichier: str, mode: str) -> bool:
    try:
        with open(fichier, mode) as f:
            writer = csv.writer(f, delimiter=',')
            for line in liste:
                writer.writerow(line)
        return True
    except:
        return False

def exportToJSONFile(liste: list, fichier: str) -> bool:
    with open(fichier, "w") as f:
        f.write(json.dumps(liste, indent=4))
    return True

def exportToXMLFile(liste: list, fichier: str) -> bool:
    try:
        ...
        return True
    except:
        return False

def exportToText(liste: list, fichier: str) -> bool:
    try:
        with open(fichier, "w") as f:
            for line in liste:
                f.write(str(line)+'\n')
        return True
    except:
        return False
