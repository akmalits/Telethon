from sqlalchemy.orm import Session
from . import models, schemas

def create_telethon_data(db: Session, data: schemas.TelethonDataCreate):
    db_data = models.TelethonData(content=data.content)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_all_data(db: Session):
    return db.query(models.TelethonData).order_by(models.TelethonData.timestamp.desc()).all()

def get_latest_data(db: Session):
    return db.query(models.TelethonData).order_by(models.TelethonData.timestamp.desc()).first()