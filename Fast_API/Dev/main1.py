from fastapi import FastAPI, Response
from pydantic import BaseModel, validator
from datetime import date, datetime, time, timedelta
from enum import Enum


class Doctor(BaseModel):  #Product
    lname: str
    fname: float

class KIND (str, Enum):
    follow_up = "follow_up"
    new_patient = "new_patient"


class Appointment(BaseModel):  #Product
    patientname: str
    date: date
    kind: KIND
    time: time
    #New appointments can only start at 15 minute intervals
    @validator("time")
    def ensure_time_is_at_15min_interval(cls, given_time):
        #let's assume the time is regular time (NOT MILITARY TIME)
        if ("15"  not in given_time or
             "00" not in given_time or
             "30" not in given_time or
             "45" not in given_time):
            raise ValueError("Time not in required interval")
        return time

doctors = [
    {"id": 1, "lname": "Nelson", "fname": "Nick"},
    {"id": 2, "lname": "Jep", "fname": "Mercy"}
 
]

appointments = [
    {"id": 1, "doctor_id": 2, "patientname": "Akuku Danger", "date": "08/09/22", "time": "08:30PM"},
 
]

app = FastAPI()


@app.get("/doctors")
def get_all_doctors():
    return doctors

@app.get("/doctors/{id}/appointments/day")
def index(id: int, day:str):
    
    for doctor in doctors:
        if doctor["id"] == id:
            doctor_id = doctor["id"]
    if not doctor_id: 
        return "Doctor Not Found"
    
    appt_lists = []
    for appt in appointments:
        if (appt["doctor_id"] == doctor_id 
            and appt["date"] == day):
            appt_lists.append(appt)
    
    if len(appt_lists) == 0: 
        return "No appointments Found for this Doctor"

    return appt_lists


@app.delete("/doctors/{doctor_id}/appointments/{appt_id}")
def delete_appointment(doctor_id:int, appt_id:int,  response: Response):
    for appt in appointments:
        if appt["doctor_id"] == doctor_id:
            if appt["id"] == appt_id:
                appointments.remove(appt)
                return "Appointment Deleted"
    
    return "Appointment or Doctor Not Found"
  

@app.post("/doctors/{doctor_id}/appointments")
def create_appointment(doctor_id:int, time:time,  new_appointment: Appointment, response: Response):

    #A doctor can have multiple appointments with the same time, but no more than 3 
    def check_number_of_appointments_at_particular_time(time:time, doctor_id:int):
        count_appts = 0
        for appt in appointments:
            if (appt["doctor_id"] == doctor_id and
                appt["time"] == time):
                count_appts+=1
        return count_appts

    sametime_apptNumbers = check_number_of_appointments_at_particular_time(time, doctor_id)

    if sametime_apptNumbers <= 3:
        appointment = new_appointment.dict()
        appointment["id"] = len(appointments)+1
        appointments.append(appointment)
        return appointment
