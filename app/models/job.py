from sqlalchemy import Column, Integer, String, Text
from app.db.session import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    skills_extracted = Column(Text, nullable=True)  # On stockera ici le JSON des compétences