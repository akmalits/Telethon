import os  # Import os module
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Get allowed origins from environment variable
allow_origins = os.getenv("ALLOW_ORIGINS", "*").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Use environment variable for allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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