# UE-AD-A1-REST

# 🪪 Description du projet

Ce projet est une application de réservation de séances de cinéma. L'application est composée de 4 services qui
communiquent entre eux.

✨ Le projet a été réalisé dans le cadre du cours Architectures Distribuées A1 à l'IMT Atlantique par Matis BYAR et
Julien NGUYEN.

Il est identique à la version Mixte qui utilise différentes technologies pour communiquer entre les services. Ici, les
services communiquent entre eux via des appels REST.

# 🗺️ Architecture du projet

Le projet est divisé en plusieurs dossiers qui représentent les différents services de l'application.

- `movie` : Service de gestion des films (port 3200)
- `booking` : Service de réservation (port 3201)
- `showtime` : Service de gestion des séances (port 3202)
- `user` : Service de gestion des utilisateurs (port 3203)

![Architecture du projet](https://helene-coullon.fr/images/rest-22-23.png)

# ▶️ Comment lancer le projet

De prime abord, il faut installer les dépendances de chaque service. Pour cela, il suffit de lancer la commande suivante
dans chaque dossier :

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Pour lancer le projet, il suffit de lancer les commandes suivantes dans 4 terminaux différents :

```bash
cd movie
python movie.py
```

```bash
cd booking
python booking.py
```

```bash
cd showtime
python showtime.py
```

```bash
cd user
python user.py
```

# 🚀 Utilisation de l'application

Tous les services ont une documentation disponibles dans les répertoires associés :

- [Booking](booking/UE-archi-distribuees-Booking-1.0.0-resolved.yml)
- [Movie](movie/UE-archi-distribuees-Movie-1.0.0-resolved.yml)
- [Showtime](showtime/UE-archi-distribuees-Showtime-1.0.0-resolved.yml)
- [User](user/UE-archi-distribuees-User-1.0.0-resolved.yml)