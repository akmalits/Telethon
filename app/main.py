from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/data/", response_model=schemas.TelethonDataResponse)
def create_data(data: schemas.TelethonDataCreate, db: Session = Depends(get_db)):
    return crud.create_telethon_data(db, data)

@app.get("/data/", response_model=list[schemas.TelethonDataResponse])
def read_all_data(db: Session = Depends(get_db)):
    return crud.get_all_data(db)

@app.get("/data/latest/", response_model=schemas.TelethonDataResponse)
def read_latest_data(db: Session = Depends(get_db)):
    data = crud.get_latest_data(db)
    if data is None:
        raise HTTPException(status_code=404, detail="No data found")
    return data