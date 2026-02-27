import os
import pandas as pd
import numpy as np  # <--- Ajouté pour gérer les NaN
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Charger le .env
load_dotenv()

# Récupérer l'URL de connexion
DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("La variable DATABASE_URL n'est pas définie dans .env")

# Créer le moteur SQLAlchemy
engine = create_engine(DB_URL, fast_executemany=True)

# Lire le CSV
df = pd.read_csv('ml/data/clean_jobs_with_skills.csv')

# --- NETTOYAGE DES DONNÉES ---
# Remplace les NaN (flottants invalides pour SQL) par None (NULL SQL)
df = df.replace({np.nan: None})
# -----------------------------

# Créer la table si elle n'existe pas
with engine.begin() as conn:
    conn.execute(text("""
    IF NOT EXISTS (
        SELECT * FROM sysobjects WHERE name='jobs' AND xtype='U'
    )
    CREATE TABLE jobs (
        id INT IDENTITY(1,1) PRIMARY KEY,
        job_title NVARCHAR(255),
        skills_extracted NVARCHAR(MAX)
    )
    """))

# Insérer les données
with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(text("""
            INSERT INTO jobs (job_title, skills_extracted)
            VALUES (:job_title, :skills_extracted)
        """), {
            "job_title": row["Job Title"],
            "skills_extracted": row["extracted_skills"]
        })

print(f"{len(df)} offres insérées dans Azure SQL 🎉")