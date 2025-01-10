# Étape 1: Utiliser l'image officielle Python comme base
FROM python:3.10-slim

# Étape 2: Définir le répertoire de travail
WORKDIR /app

# Étape 3: Copier le fichier des dépendances
COPY ./user_management_service/requirements.txt . 
# Assurez-vous que le chemin est correct

# Étape 4: Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier le code source de l'application
COPY ./user_management_service/ .  
# Assurez-vous que tous les fichiers sont dans ce dossier

# Étape 6: Exposer le port 8000 (ou celui que vous utilisez)
EXPOSE 8000

# Étape 7: Lancer l'application avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
