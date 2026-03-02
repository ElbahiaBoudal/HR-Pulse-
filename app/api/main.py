from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import joblib
from app.db.session import Base, engine, get_db
# Imports internes (assurez-vous que ces fichiers existent)
import pandas as pd
from app.models.job import Job
from app.models.user import User

from app.schemas.users import UserRegistre  # Import du schéma Pydantic
from app.authentification.security import hash_password, verify_password
from app.authentification.auth import create_access_token,verify_token
from app.schemas.predection import SalaryPrediction,SalaryFeatures
from fastapi.middleware.cors import CORSMiddleware

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import os

Base.metadata.create_all(bind=engine)
app = FastAPI(title="HR-Pulse API")

# -------------------------
# OpenTelemetry Configuration
# -------------------------

resource = Resource.create({
    "service.name": "hr-pulse-backend"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)



otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
    insecure=True
)

provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Instrumentation automatique
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Chargement du modèle
model = joblib.load("app/salary_model.pkl")

# Sécurité
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        username = verify_token(token)  # decode JWT et récupère le username
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non autorisé")
    return user

### Authentification & Utilisateurs

@app.post("/register")
def register(user: UserRegistre, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    # Hachage
    hashed = hash_password(user.password)

    # Création de l'utilisateur
    new_user = User(
        username=user.username,
        email=user.email,  # Assure-toi qu'il n'est pas None
        hashed_password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Username ou password incorrect")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/jobs")
def get_jobs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Job).limit(50).all()


@app.get("/search")
def search(skill: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.skills_extracted.contains(skill)).all()




@app.post("/predict", response_model=SalaryPrediction)
def predict_salary(data: SalaryFeatures, current_user: User = Depends(get_current_user)):
    # Créer un dataframe avec la même structure que celui utilisé pour l'entraînement
    df_input = pd.DataFrame([{
        "text": f"{data.job_title} {data.job_description}",  # concaténation
        "Rating": data.rating,
        "Location": data.location,
        "Size": data.size,
        "Industry": data.industry,
        "Sector": data.sector,
        "Founded": data.founded
    }])

    # Prédiction
    pred = model.predict(df_input)
    
    return SalaryPrediction(salary_prediction=float(pred[0]))