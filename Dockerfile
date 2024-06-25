# Utiliser l'image de base Python 3.10
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /home/PRED

# Mettre à jour pip et setuptools
RUN pip install --upgrade pip setuptools

# Copier le fichier de configuration des dépendances
COPY requirements.txt /home/PRED/

# Installer les dépendances à partir du fichier requirements.txt
RUN pip install -r requirements.txt

# Installer gunicorn
RUN pip install gunicorn

# Copier le reste du code source
COPY . /home/PRED/

# Exposer le port de l'application
EXPOSE 8080

# Commande de démarrage de l'application
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080", "--worker-class", "uvicorn.workers.UvicornWorker"]
