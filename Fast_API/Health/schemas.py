
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date, time

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
   

class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    #id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_name: str
    time: datetime
    kind: str
   

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    patient_name: str
    time: str
    kind: str
    
    class Config:
        orm_mode = True