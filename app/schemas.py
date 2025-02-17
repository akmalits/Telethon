from pydantic import BaseModel
from datetime import datetime

class TelethonDataCreate(BaseModel):
    content: str

class TelethonDataResponse(BaseModel):
    id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True