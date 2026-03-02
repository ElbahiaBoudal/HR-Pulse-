FROM python:3.12-slim

WORKDIR /app

# Installation des outils nécessaires
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Installation des dépendances système (indispensable pour pyodbc/sql server)
# Installation du Driver Microsoft ODBC 18 et des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    build-essential \
    libgomp1 \
    unixodbc-dev && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de configuration
COPY pyproject.toml uv.lock ./

# Synchronisation des dépendances (installe python-dotenv si ajouté au toml)
RUN uv sync --frozen --no-dev

# Copie du reste du code source
COPY . .

# IMPORTANT : On utilise 'uv run' pour que l'environnement soit chargé correctement
CMD ["uv", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]