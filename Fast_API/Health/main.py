
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import models,schemas
from db import get_db, engine


from crud import DoctorRepo, AppointmentRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.post('/doctors', tags=["Doctor"],response_model=schemas.Doctor,status_code=201)
async def create_doctor(doctor_request: schemas.DoctorCreate, db: Session = Depends(get_db)):

    db_doctor = DoctorRepo.fetch_by_name(db, name=doctor_request.last_name)
    print(db_doctor)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await DoctorRepo.create(db=db, doctor=doctor_request)

@app.get('/doctors', tags=["Doctor"],response_model=List[schemas.Doctor])
def get_all_doctors(name: Optional[str] = None, db: Session = Depends(get_db)):
  
    if name:
        items = []
        db_item = DoctorRepo.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return DoctorRepo.fetch_all(db)


#Appointments
@app.post('/appointments', tags=["Appointment"],response_model=schemas.Appointment,status_code=201)
async def create_appointment(appt_request: schemas.AppointmentCreate, 
                             db: Session = Depends(get_db)):
    
    db_patientName = AppointmentRepo.fetch_by_name(db, name=appt_request.patient_name)
    print({'name':db_patientName})

    # db_appointmentTime = AppointmentRepo.fetch_by_name(db, name=appt_request.time)
    # print({'time': db_appointmentTime})
    
    #if appointment time and appointment doctor are all same row (same row id, then it appt exists)
    if db_patientName:
        raise HTTPException(status_code=400, detail="Appointment already exists!")

    return await AppointmentRepo.create(db=db, appointment=appt_request)



