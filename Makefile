# Makefile final, utilisant directement les exécutables du venv et prévenant les conflits

# --- Variables ---
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

DOCKER_CONTAINER_NAME := pubsub-server
CLIENT_SCRIPT := main.py

# --- Cibles ---
.PHONY: help run run-server run-client stop-server force-update setup-venv force-rebuild

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Cibles disponibles :"
	@echo "  setup-venv    Crée l'environnement virtuel et installe les dépendances."
	@echo "  run           Nettoie, lance le serveur et le client."
	@echo "  run-server    Nettoie puis lance le serveur via Docker Compose."
	@echo "  run-client    Lance le script client Python en utilisant le venv."
	@echo "  stop-server   Arrête les services Docker Compose."
	@echo "  force-update  Force la mise à jour des dépendances du client."

# Tâche principale
# CORRECTION : Ajout de la dépendance 'stop-server' pour nettoyer avant de lancer
run: stop-server
	@echo "-> Lancement du serveur en arrière-plan (via docker compose)..."
	@docker compose up -d --build
	@echo "-> Attente de 5 secondes que le serveur démarre..."
	@sleep 5
	@make run-client
	@echo "-> Arrêt du serveur..."
	@make stop-server

# Lance le serveur en avant-plan
# CORRECTION : Ajout de la dépendance 'stop-server' pour nettoyer avant de lancer
run-server: stop-server
	@echo "-> Lancement du serveur en avant-plan (via docker compose)..."
	@docker compose up --build

# Lance le client en utilisant le python du venv
run-client:
	@echo "-> Lancement du client Python avec l'interpréteur du venv..."
	@$(PYTHON) $(CLIENT_SCRIPT)

# Arrête le serveur
stop-server:
	@echo "-> Arrêt et suppression des conteneurs (via docker compose)..."
	@docker compose down --rmi all || true
	# @docker compose down
	# @docker rm -f pubsub-server

# Force la mise à jour des dépendances en utilisant le pip du venv
force-update:
	@echo "-> Nettoyage du cache pip..."
	@$(PIP) cache purge
	@echo "-> Mise à jour des dépendances client depuis requirements.txt..."
	@$(PIP) install --no-cache-dir -r requirements.txt

# CIBLE : Pour la configuration initiale
setup-venv:
	@echo "-> Création de l'environnement virtuel..."
	@python3 -m venv $(VENV_DIR)
	@echo "-> Installation des dépendances dans le venv..."
	@$(PIP) install -r requirements.txt
	@echo "-> Environnement prêt ! Vous pouvez maintenant utiliser 'make run'."

# NOUVELLE CIBLE : Pour forcer la reconstruction sans utiliser le cache
force-rebuild: stop-server
	@echo "-> Lancement d'une reconstruction complète SANS CACHE..."
	@docker compose build --no-cache
	@echo "-> Lancement du serveur en arrière-plan..."
	@docker compose up -d
	@echo "-> Serveur lancé. Vous pouvez maintenant utiliser 'make run-client'."
