# Image de base légère Python 3.12
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Copie d'abord les dépendances pour optimiser le cache Docker
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code
COPY . .

# Expose le port de l'API
EXPOSE 5000

# Lance l'application
CMD ["python", "app.py"]
