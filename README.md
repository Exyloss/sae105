# sae105

---

# Sommaire

1. Explication du contenu du log apache
2. Structures python utilisées
3. Fonctionnement de l'analyse du journal apache
4. Utilisation de [ip-api.com](https://ip-api.com)
5. Création des statistiques
6. Génération de la carte

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

# 3. Fonctionnement de l'analyse du journal apache

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

# 5. Création des statistiques

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
