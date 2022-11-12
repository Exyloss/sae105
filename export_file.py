import json
import csv
import xml.etree.ElementTree as et
import xml.dom.minidom

def exportToCSVFile(liste: list, fichier: str) -> bool:
    try:
        with open(fichier, "w") as f:
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
    data = et.Element('root')
    elts = []
    for line in liste:
        elts.append(et.SubElement(data, 'request'))
        et.SubElement(elts[-1], 'ip').text        = line[0]
        et.SubElement(elts[-1], 'date').text      = line[1]
        et.SubElement(elts[-1], 'http_code').text = line[2]
        et.SubElement(elts[-1], 'system').text    = line[3]
        et.SubElement(elts[-1], 'browser').text   = line[4]

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
