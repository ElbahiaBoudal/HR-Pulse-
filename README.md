
---

# 🚀 HR-Pulse Backend - AI Job Analyzer

Ce repository contient le cœur logique de la solution **HR-Pulse**. Il s'agit d'une API de traitement d'offres d'emploi automatisée par IA, capable d'extraire des compétences via NER (Named Entity Recognition) et de prédire des fourchettes salariales.

## 🛠️ Stack Technique

* **Gestionnaire de paquets :** `uv` (remplace pip)
* **Framework API :** FastAPI
* **Intelligence Artificielle :** Azure AI Language (Extraction d'entités)
* **Base de données :** Azure SQL (via SQLAlchemy & pyodbc)
* **Observabilité :** OpenTelemetry + Jaeger
* **Conteneurisation :** Docker

---

## 📋 Prérequis

1. Avoir installé [uv](https://github.com/astral-sh/uv).
2. Un accès au groupe de ressources Azure (fourni par l'architecte).
3. Docker et Docker Compose installés localement.

---

## 🚀 Installation & Lancement Local

### 1. Configuration de l'environnement

Clonez le repo et créez votre environnement virtuel avec `uv` :

```bash
uv venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
uv sync

```

### 2. Variables d'environnement

Créez un fichier `.env` à la racine :

```ini
DATABASE_URL=mssql+pyodbc://<user>:<password>@<server>.database.windows.net/hr_db?driver=ODBC+Driver+18+for+SQL+Server
AZURE_AI_KEY=votre_cle_azure
AZURE_AI_ENDPOINT=votre_endpoint_azure
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

```

### 3. Lancement de l'API

```bash
uv run uvicorn main:app --reload

```

L'API sera disponible sur : `http://localhost:8000/docs` (Swagger UI).

---

## 🏗️ Infrastructure (Terraform)

Le provisioning des ressources Azure est automatisé.

```bash
cd terraform
terraform init
terraform apply

```

---

## 🐳 Docker & Observabilité

Pour lancer le backend avec Jaeger pour le monitoring des traces :

```bash
docker-compose up -d

```

* **Backend :** `http://localhost:8000`
* **Jaeger UI :** `http://localhost:16686` (Pour visualiser la latence SQL et IA)

---

## 🧪 Tests & Qualité

Avant chaque commit, assurez-vous que le code respecte les standards :

* **Linting (Ruff) :** `uv run ruff check .`
* **Tests Unitaires (Pytest) :** `uv run pytest`

---

## 📂 Structure du Projet

* `/app` : Code source FastAPI.
* `/models` : Modèles de données SQL et schémas Pydantic.
* `/services` : Logique métier (Appels Azure AI, Predictor ML).
* `/tests` : Tests unitaires et d'intégration.
* `Dockerfile` : Configuration de l'image optimisée.

---
