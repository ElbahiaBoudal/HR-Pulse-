from pydantic import BaseModel
from typing import List, Optional

class JobResponse(BaseModel):
    id: int
    job_title: str
    skills_extracted: List[str]  # ou str si tu stockes JSON
   