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
    async def create(db: Session, appointment: schemas.AppointmentCreate, doctor_id:int):
        db_appt = models.Appointment(patient_name = appointment.patient_name,
                                     time = appointment.time,
                                     kind = appointment.kind,
                                     doctor_lname = appointment.doctor_lname,
                                     doctor_fname = appointment.doctor_fname
                                )

        db.add(db_appt)
        db.commit()
        db.refresh(db_appt)
        return db_appt
    
        
    def fetch_by_id(db: Session,_id:int):
        return db.query(models.Appointment).filter(models.Appointment.id == _id).first()
    
    def fetch_by_name(db: Session,name:str):
        return db.query(models.Appointment).all()
        #return db.query(models.Appointment).filter(models.Appointment.doctor_lname == name).first()
    
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Store).offset(skip).limit(limit).all()
    
    async def delete(db: Session,_id:int):
        db_store= db.query(models.Appointment).filter_by(id=_id).first()
        db.delete(db_store)
        db.commit()
        
    async def update(db: Session,store_data):
        db.merge(store_data)
        db.commit()