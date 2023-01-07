from sqlalchemy import Column,Integer, String, Date, ForeignKey

from database import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    
    hospital_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String, index=True,nullable=False)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    password = Column(String,nullable = False)

class Staff(Base):
    __tablename__ = "staffs"
    
    staff_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=True)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    staff_role = Column(String,nullable=True)
    password = Column(String,nullable = False)

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=False)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)

class Donor(Base):
    __tablename__ = "donors"
    
    donor_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=False)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)

class Repository(Base):
    __tablename__ = "repository"

    blood_id = Column(String, primary_key=True, index=True,nullable=False)
    blood_group = Column(String,nullable=True)
    plasma = Column(Integer,nullable=True)
    platelets = Column(Integer,nullable=True)
    rbc = Column(Integer,nullable=True)

class Request(Base):
    __tablename__ = "requests"

    request_id = Column(String, primary_key=True, index=True,nullable=False)
    hospital_id = Column(String, ForeignKey("hospitals.hospital_id"),nullable=True)
    patient_case = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    blood_component = Column(String,nullable=True)
    quantity = Column(Integer,nullable=True)
    status = Column(String,nullable=True,default="pending")

class Donation(Base):
    __tablename__ = "donations"

    donation_id = Column(String, primary_key=True, index=True,nullable=False)
    donor_id = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    quantity = Column(Integer,nullable=True)
    donation_occasion = Column(String,nullable=True)
    donation_date = Column(Date,nullable=True)