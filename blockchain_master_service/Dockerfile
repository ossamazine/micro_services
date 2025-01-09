# Étape 1: Utiliser l'image officielle Python comme base
FROM python:3.9-slim

# Étape 2: Définir le répertoire de travail
WORKDIR /app

# Étape 3: Copier le fichier des dépendances
COPY blockchain_master_service/requirements.txt .
# Assurez-vous que le fichier se trouve dans ce dossier

# Étape 4: Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier le code source de l'application
COPY blockchain_master_service/ .
# Assurez-vous que tous les fichiers sont dans ce dossier

# Étape 7: Exposer le port 8000 (ou 8001 si c'est celui que vous utilisez)
EXPOSE 8001

# Étape 8: Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
