# sae105

---

# Sommaire

1. Explication du contenu du log apache
2. Structures python utilisées
3. Fonctionnement de l'analyse du journal apache
4. Utilisation de [ip-api.com](https://ip-api.com)
5. Création des statistiques
6. Génération de la carte
7. Annexe

---

# 1. Explication du contenu du log apache

Prenons un exemple de ligne :

```log
1.2.3.4 - - [09/Nov/2021:00:11:19 +0100] "GET /fr/ HTTP/1.1" 200 312540 
"https://controltower.fr/fr" 
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
```

Sur cette ligne, les informations sont séparées par des espaces et des guillemets sont utilisées afin de délimiter les données. Nous pouvons
ici lire les informations suivantes :

1. L'adresse IP du client, ici 1.2.3.4
2. L'identité du client, le serveur apache2 n'utilise pas cette fonctionnalité car la donnée est un tiret
3. L'identifiant utilisateur du client, le serveur ne l'utilise pas
4. La date de la requête et le fuseau horaire, celle-ci est mise entre crochets
5. le type de requête, la ressource demandée et la version du protocole, ici c'est une requête GET de la page /fr/ du serveur apache avec
la version 1.1 du protocole HTTP
6. Code de retour HTTP, ici cette valeur est 200, donc la requête est un succès
7. La taille de l'objet retourné au client, ici 312.54ko.
8. Adresse de la requête HTTP
9. User-agent, cette valeur nous indique quel est le système d'exploitation du client, ici Ubuntu, et quel est le navigateur du client, ici
Firefox.

# 2. Structures python utilisées

Pour organiser les données parcourues, nous utilisons un tableau à deux dimensions. Les sous-tableaux peuvent contenir les données
renseignées par l'utilisateur, c'est-à-dire l'ip, la date, le système d'exploitation ou le navigateur. Ces données sont ensuite transcrites dans un fichier
csv/json/xml.

# 3. Fonctionnement de l'analyse du journal apache

Pour analyser le fichier de log apache, nous avons utilisé dans regular expressions (ou regex). Ces regex nous permettent d'obtenir une chaîne de caractère qui respècte
un certain pattern. Par exemple, pour la date, la regex suivante permet de récupérer les valeurs entre crochets : "\\[.\*?\\]". Voici les différentes regex que nous
avons utilisé :

- "\\[.\*?\\]" pour la date
- " [0-9]{3} " pour le code HTTP, une chaîne de trois chiffres entourée par des espaces
- "\\(.\*?\\)" pour le système d'exploitation, une valeur entre parenthèses
- browser+'\\/.\*?(?:"| )' pour le navigateur, browser est son nom mais le regex renvoie nom/version
- pour obtenir une version simplifiée de l'OS, on récupère le nom de l'OS, puis pour la version on utilise par exemple ce regex : "Android \\d{1,2}"

# 4. Utilisation de [ip-api.com](https://ip-api.com)

Pour nous servir de cette API, nous avons simplement étudié la documentation officelle de celle-ci disponible 
[ici](https://ip-api.com/docs/api:json).

En consultant la documentation, nous apprenons que pour récupérer les informations d'un adresse IP, nous devons
réaliser une requête GET de l'adresse https://ip-api.com/json/{adresse-ip}. Nous avons alors essayé cette API à
l'aide de la commande curl suivante :

```bash
curl -X GET https://ip-api.com/json/24.48.0.1?fields=status,lat,lon
```

En lançant cette commande, nous pouvons voir les données renvoyées par l'API. Les valeurs retournées sont celles renseignées dans le paramètre
fields de la requête. Ici, le serveur renverra le statut de la requête (si elle a réussi ou échoué), la latitude et la longitude
de la position de l'adresse IP renseignée.

Alors, nous avons transcrit cette requête en python :

```python
import requests
import json

def getIP_infos(ip: str) -> dict:
    url = "http://ip-api.com/json/"
    response = requests.get(url+ip)
    data = response.content
    values = json.loads(data)
    return values
```

# 5. Création des statistiques

Les statistiques ont été réalisées avec matplotlib.pyplot pour les camemberts et pandoc pour les histogrammes, les graphiques générés sont visionables dans le répertoire img/

# 6. Génération de la carte

Afin de générer la carte des visiteurs, nous avons utilisé la librairie python «folium» :

```bash
pip install folium
```

Cette librairie a comme avantage d'être très simple d'utilisation. En effet, pour utiliser cette librairie, il faut
instancier l'objet Map comme ceci :

```python
m = folium.Map(location=[50, 0], zoom_start=5)
```

Puis, pour placer des points, il faut instancier des objets Marker et appeller leur méthode add_to afin de les ajouter
sur la carte :

```python
folium.Marker((lat, lon)).add_to(m)
```

Enfin, nous pouvons sauvegarder cette carte avec la méthode save de l'objet Map :

```python
m.save("index.html")
```

# 7. Annexe

1. Fonction parse :

```python
def parse(file: str, filter_bot: bool = False, uniq: bool = False) -> list:
    lines = open(file, 'r').readlines()
    tab = []
    ip_list = []
    for line in lines:
        ip = line.split(" ")[0]
        if not uniq or ip not in ip_list:
            ip_list.append(ip)
            date = re.findall(r"\[.*?\]", line)[0]
            exit_code = re.findall(" [0-9]{3} ", line)[0][1:-1]
            browser = get_browser(line)
            try:
                systeme = get_system(re.findall("\(.*?\)", line)[0])
            except:
                systeme = "Unknown"
            if filter_bot == False or (browser != "Robot" and "http" not in systeme):
                tab.append([ip, date, exit_code, systeme, browser])
    return tab
```

cette fonction retourne un tableau à deux dimensions contenant les données suivantes de gauche à droite : ip, date, code HTTP, système d'exploitation, navigateur.
Pour obtenir les données recherchées, elle utilise une regex par valeur puis ajoute le tableau de ces valeurs à la fin du tableau principal. Les paramètres
filter_bot et uniq permettent respectivement de retirer les bots ou de faire que chaque IP soit unique dans le tableau retourné.

2. Fonction get_browser :

```python
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
```

Cette fonction retourne le nom du navigateur et sa version séparés par un "/". Le paramètre de cette fonction est une ligne du fichier de log apache.
Tout d'abord, la fonction sépare le user-agent (c'est-à-dire les informations sur les logiciels du client) afin de rechercher le navigateur du client.
Pour ce faire, on vérifie si le nom de chaque navigateur populaire est présent dans le user-agent. s'il y est, on assigne son nom à la variable browser.
Puis, si le navigateur est reconnu, on retourne le navigateur et sa version à l'aide d'une regex.

3. Fonction get_system :

```python
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
```

Cette fonction retourne le nom du système d'exploitation du client et sa version séparés par un espace. Pour obtenir la version, nous avons utilisé une autre regex,
celle-ci détecte les entiers de un ou deux chiffres présents après le nom du système d'exploitation.

4. Fonction ip_infos :

```python
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
```

Cette fonction sert à lire les informations de l'adresse IP telles que la position de celle-ci, son pays, et son fournisseur d'accès internet. Elle
a notamment servit à réaliser l'histogramme des nationalités et la carte des IP.

5. Fonction get_data :

```python
def get_data(liste: list, data: list) -> list:
    data_dic = {"ip": 0, "date": 1, "http_code": 2, "browser": 4, "system": 3}
    index = []
    for i in data:
        index.append(data_dic[i])

    tab = []
    n = len(index)
    for line in liste:
        if n > 1:
            tab.append([])
            for i in index:
                tab[-1].append(line[i])
        else:
            tab.append(line[index[0]])
    return tab
```

Cette fonction conserve seulement les données demandées par l'utilisateur du programme en ligne de commande. liste est la liste générée par la fonction
parse et data est la liste des données voulues par l'utilisateur. index est un tableau contenant l'index des valeurs voulues par l'utilisateur dans liste.
Le tableau liste est parcourut et les données présentes aux index présents dans le tableau index sont insérées dans les sous-tableaux du tableau tab qui
est enfin retourné.

6. Fonction print_tab :

```python
def print_tab(liste: list) -> None:
    is_tab = isinstance(liste[0], list)
    for line in liste:
        if is_tab:
            print("|".join(line))
        else:
            print(line)
```

Cette fonction affiche les données d'un tableau à deux dimension en séparant les colonnes par un tube.

7. Les fonctions browser_stat et system_stat :

Ces fonctions listent les navigateurs ou systèmes d'exploitation et leurs versions avec leurs nombres d'apparition dans le tableau renseigné en paramètre.
