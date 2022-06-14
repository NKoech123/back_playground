from sqlalchemy.orm import Session

import models, schemas

class DoctorRepo:
    
 async def create(db: Session, doctor: schemas.DoctorCreate):
        db_item = models.Doctor(first_name = doctor.first_name,
                                last_name = doctor.last_name)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
 def fetch_by_id(db: Session,_id):
     return db.query(models.Doctor).filter(models.Doctor.id == _id).first()
 
 def fetch_by_name(db: Session, name):
     return db.query(models.Doctor).filter(models.Doctor.last_name == name).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Doctor).offset(skip).limit(limit).all()
 
 async def delete(db: Session,item_id):
     db_item= db.query(models.Doctor).filter_by(id=item_id).first()
     db.delete(db_item)
     db.commit()
     
 async def update(db: Session,item_data):
    updated_item = db.merge(item_data)
    db.commit()
    return updated_item


class AppointmentRepo:
    async def create(db: Session, doctor: schemas.AppointmentCreate):
        db_appt = models.Doctor(first_name = doctor.first_name,
                                last_name = doctor.last_name)

        db.add(db_appt)
        db.commit()
        db.refresh(db_appt)
        return db_appt
    