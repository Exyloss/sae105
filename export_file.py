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
    try:
        with open(fichier, "w") as f:
            f.write("[\n")
            for item in liste:
                json.dump(item, f)
                f.write(',\n')
            f.write(']')
        return True
    except:
        return False

def exportToXMLFile(liste: list, fichier: str) -> bool:
    try:
        ...
        return True
    except:
        return False
