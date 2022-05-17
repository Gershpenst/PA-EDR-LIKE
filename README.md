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

Si la variable `SECURE_MODE` est en `True` (mode `HTTPS`), il faudra générer le certificat du serveur. Nous allons créer un CA afin de créer le serveur.
```bash
$ cd certificate
$ # Generate CA certificate and private key
$ openssl genrsa 2048 > ca.key
$ openssl req -new -x509 -nodes -days 365000 -key ca.key -out ca.crt -subj "/C=FR/ST=Paris/L=Ile-de-France/O=/OU=/CN=PA-CA/emailAddress=admin@admin.com"

$ # Generate server certificate and private key
$ openssl req -newkey rsa:2048 -nodes -days 365000 -keyout server.key -out server.csr -subj "/C=FR/ST=Paris/L=Ile-de-France/O=/OU=/CN=PA-SERVER/emailAddress=admin@admin.com"
$ openssl x509 -req -days 365000 -set_serial 01 -in server.csr -out server.crt -CA ca.crt -CAkey ca.key 

$ # Verifying certificate
$ openssl verify -CAfile ca.crt ca.crt server.crt
```

La variable `VERIFIED_USER` permet de connecter les clients possédant le certificat généré par notre CA. Cela veut dire que si cette variable est à `True`, l'utilisateur ne possédant pas de certificat donné par notre CA, ne pourra pas communiquer avec notre API.
```bash
$ cd certificate
$ # Generate client certificate and private key
$ openssl req -newkey rsa:2048 -nodes -days 365000 -keyout client.key -out client.csr -subj "/C=FR/ST=Paris/L=Ile-de-France/O=/OU=/CN=PA-CLIENT/emailAddress=admin@admin.com"
$ openssl x509 -req -days 365000 -set_serial 01 -in client.csr -out client.crt -CA ca.crt -CAkey ca.key

$ # Verifying certificate
$ openssl verify -CAfile ca.crt ca.crt client.crt
```

> :warning: **Whatever method you use to generate the certificate and key files, the Common Name value used for the server and client certificates/keys must each differ from the Common Name value used for the CA certificate. Otherwise, the certificate and key files do not work for servers compiled using OpenSSL.**:

## Execution du serveur
```bash
$ python3 main.py
```
