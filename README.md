### EDR LIKE

## Pré-requis 
- python3, pip3
- mongodb installé (ou container)
- Compte chez Virus Total

## Installation des packages python3
```bash
$ pip3 install Flask Flask-Cors pymongo
```

## Modification des variables d'environnement
Dans le dossier `env` se trouve trois fichiers permettant au bon fonctionnement de l'application.
```bash
cd env/
```

# Variable d'environnement pour Mongodb
```bash
$ cp .mongodb_env.py mongodb_env.py 
```
Puis modifier les données qui y sont présent.
```python
MONGODB_DOMAIN = "localhost"
MONGODB_PORT = 27017
MONGODB_USERNAME = "<USERNAME>"
MONGODB_PASSWORD = "<SECURE_PASSWORD>"
```

# Variable d'environnement pour communiquer avec Virus Total
```bash
$ cp .virustotal_env.py virustotal_env.py 
```
Puis modifier les données qui y sont présent. La donnée `<API_TOKEN_VT>` se trouve dans le compte de Virus Total.
```python
URL_VT = "https://www.virustotal.com/api/v3"
API_TOKEN_VT = "<API_TOKEN_VT>"
```

# Variable d'environnement du serveur FLASK
```bash
$ cp .server_env.py server_env.py 
```
Puis modifier les données qui y sont présent. La donnée `<API_TOKEN_VT>` se trouve dans le compte de Virus Total.
```python
HOSTNAME_FLASK = "0.0.0.0"
PORT_FLASK = 4444
SECURE_MODE = True
```

Si la variable `SECURE_MODE`est en `True` : 
```bash
$ cd server_ssl
$ openssl req -x509 -newkey rsa:4096 -nodes -out server.crt -keyout server.key -days 365
```

NB : `SECURE_MODE` active le `HTTPS`.

## Execution du serveur
```bash
$ python3 main.py
```
