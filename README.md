# Client de Démonstration Pub/Sub Python

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

Ce projet est une démonstration complète d'un client Pub/Sub en Python. Il utilise le client `Python.PubSub.Client` pour interagir avec un serveur Pub/Sub qui est
automatiquement lancé via **Docker Compose**. L'ensemble du processus, du démarrage du serveur à l'exécution du client, est orchestré par un **`Makefile`**, simplifiant
radicalement l'utilisation et les tests.

## ✨ Fonctionnalités de cette démonstration

- 🚀 **Orchestration Simplifiée** : Un `Makefile` complet pour gérer l'ensemble du cycle de vie de l'application (installation, lancement, arrêt).
- 🐳 **Serveur Conteneurisé** : Le serveur Pub/Sub est construit et lancé avec Docker Compose, directement depuis son dépôt Git, garantissant un environnement propre et
  isolé.
- 🔄 **Double Rôle Client/Serveur** : Le script `main.py` agit à la fois comme **consommateur** (il écoute les messages) et comme **producteur** (il publie de nouveaux
  messages dans un thread séparé).
- 🎯 **Abonnement Multi-Sujets** : Le client s'abonne et traite des messages provenant de plusieurs sujets : `orders`, `inventory`, et `shipping`.
- ⚡ **Simulation d'Événements** : Un thread dédié publie des messages de manière asynchrone pour simuler un flux d'événements en temps réel.

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre machine :

- Python 3.9+
- Docker & Docker Compose
- GNU Make
- Git

## 🚀 Démarrage Rapide

Lancer la démonstration complète est un jeu d'enfant grâce au `Makefile`.

### Étape 1 : Configuration de l'environnement

La première fois, vous devez créer l'environnement virtuel Python et installer les dépendances. Le `Makefile` s'en charge pour vous.

```bash
make setup-venv
```

Cette commande va :

1. Créer un répertoire `.venv` contenant un environnement Python isolé.
2. Installer les bibliothèques listées dans `requirements.txt` (y compris le client Pub/Sub depuis son dépôt Git).

### Étape 2 : Lancer la démonstration complète

Une fois l'environnement prêt, exécutez la cible principale du `Makefile`.

```bash
make run
```

Cette commande magique exécute un cycle de vie complet :

1. **Nettoyage** : Arrête et supprime les anciens conteneurs Docker pour partir d'un état propre (`make stop-server`).
2. **Lancement du Serveur** : Construit l'image Docker du serveur et le lance en arrière-plan (`docker compose up -d --build`).
3. **Pause** : Attend 5 secondes pour s'assurer que le serveur est pleinement opérationnel.
4. **Lancement du Client** : Exécute le script `main.py` qui va se connecter au serveur, écouter les messages et commencer à en publier (`make run-client`).
5. **Arrêt** : Une fois que vous arrêtez le client (avec `Ctrl+C`), la commande `run` se termine et arrête proprement le serveur Docker.

Vous verrez alors dans votre terminal les logs du client, montrant les messages qu'il publie et ceux qu'il reçoit et traite.

## 🛠️ Utilisation avancée avec le Makefile

Le `Makefile` est le cœur de ce projet et fournit plusieurs cibles pour un contrôle fin du processus. C'est l'outil à privilégier pour toutes les opérations.

### Lancer uniquement le serveur

Si vous souhaitez développer le client et avoir un serveur qui tourne en permanence en avant-plan pour voir ses logs.

```bash
make run-server
```

Cette commande arrêtera d'abord tout conteneur existant, puis lancera le serveur en attachant votre terminal à ses logs. Utilisez `Ctrl+C` pour l'arrêter.

### Lancer uniquement le client

À utiliser si le serveur tourne déjà (par exemple, dans un autre terminal via `make run-server`).

```bash
make run-client
```

Cette commande exécute le script `main.py` en utilisant l'interpréteur Python de l'environnement virtuel `.venv`.

### Arrêter le serveur

Pour arrêter et supprimer proprement les conteneurs Docker du serveur.

```bash
make stop-server
```

### Forcer la reconstruction du serveur

Si vous voulez reconstruire l'image Docker du serveur sans utiliser le cache de Docker (par exemple, pour vous assurer de récupérer la dernière version du dépôt Git du
serveur).

```bash
make force-rebuild
```

### Forcer la mise à jour des dépendances

Si le `requirements.txt` a changé ou si vous voulez réinstaller les dépendances du client.

```bash
make force-update
```

## ⚙️ Comprendre la Configuration

- **`docker-compose.yml`** : Ce fichier est configuré pour construire l'image du serveur directement depuis son dépôt GitHub. Cela signifie que vous n'avez pas besoin de
  cloner le projet serveur localement. C'est une méthode propre qui garantit que vous utilisez toujours la version prévue.

- **`requirements.txt`** : Notez que la dépendance principale, `Python.PubSub.Client`, n'est pas installée depuis PyPI mais directement via Git. Cela est utile pour le
  développement ou pour utiliser une version spécifique du client.

- **`main.py`** : Ce script est l'exemple concret. Il démontre comment utiliser le `PubSubClient` pour s'abonner, enregistrer des gestionnaires de messages (handlers), et
  comment publier des messages depuis un thread séparé, ce qui en fait à la fois un producteur et un consommateur.

## 🤝 Contribution

Les contributions sont les bienvenues \! Veuillez suivre ces étapes :

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-feature`)
3. Commitez vos changements (`git commit -m 'Ajout de ma nouvelle feature'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.
