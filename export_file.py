import json
import csv
import xml.etree.ElementTree as et
import xml.dom.minidom

def exportToCSVFile(liste: list, fichier: str) -> bool:
    try:
        with open(fichier, "w") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([i for i in liste[0].keys()])
            for line in liste:
                writer.writerow([i for i in line.values()])
        return True
    except:
        return False

def exportToJSONFile(liste: list, fichier: str) -> bool:
    with open(fichier, "w") as f:
        f.write(json.dumps(liste, indent=4))
    return True

def exportToXMLFile(liste: list, fichier: str) -> bool:
    data = et.Element('root')
    for line in liste:
        elt = et.SubElement(data, 'request')
        for i in line.keys():
            et.SubElement(elt, i).text = line[i]

    b_xml = et.tostring(data)
    xmlstr = xml.dom.minidom.parseString(b_xml).toprettyxml()
    with open(fichier, 'w') as f:
        f.write(xmlstr)
    return True

def exportToText(liste: list, fichier: str) -> bool:
    try:
        with open(fichier, "w") as f:
            for line in liste:
                f.write(str(line)+'\n')
        return True
    except:
        return False
