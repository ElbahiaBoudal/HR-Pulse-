from pydantic import BaseModel



# Schéma pour la réponse
class SalaryPrediction(BaseModel):
    salary_prediction: float


class SalaryFeatures(BaseModel):
    job_title: str
    job_description: str
    rating: float
    location: str
    size: str
    industry: str
    sector: str
    founded: int    