import json
import csv
import xml

def exportToCSVFile(liste: list, fichier: str) -> bool:
    try:
        with open(fichier, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for line in liste:
                writer.writerow(line)
        return True
    except:
        return False
