from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal,get_db
from app.models.job import Job
import joblib

app = FastAPI(title="HR-Pulse API")

model = joblib.load("app/salary_model.pkl")




@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).limit(50).all()


@app.get("/search")
def search(skill: str, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.skills_extracted.contains(skill)).all()

@app.post("/predict")
def predict_salary(features: list[float]):
    pred = model.predict([features])
    return {"salary_prediction": float(pred[0])}