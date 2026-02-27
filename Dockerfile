# Dockerfile.backend
FROM python:3.12-slim

# Définit le dossier de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY pyproject.toml uv.lock ./
COPY app ./app


# Installer les dépendances via uv
RUN uv install --without-venv

# Exposer le port de l'API
EXPOSE 8000

# Commande pour lancer FastAPI avec uvicorn
CMD ["uv", "run", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]