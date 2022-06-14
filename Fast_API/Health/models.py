import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from db import Base
    
class Doctor(Base):
    __tablename__ = "doctor" #item
    
    id = Column(Integer, primary_key=True,index=True)
    first_name = Column(String(80), nullable=False, unique=True,index=True)
    last_name = Column(String(80), nullable=False, unique=True,index=True)
    appointments = relationship("Appointment")
    def __repr__(self):
        return 'Doctor(first_name=%s, last_name=%s)' % (self.first_name, self.last_name)
    
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True,index=True)
    patient_name = Column(String(80), nullable=False, unique=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    kind = Column(String(20), nullable=False, unique=True,index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))


    def __repr__(self):
        return 'Store(name=%s)' % self.name
