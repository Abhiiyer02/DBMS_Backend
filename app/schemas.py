from pydantic import BaseModel, EmailStr
from datetime import date

class HospitalBase(BaseModel):
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True

class HospitalIn(HospitalBase):
    password: str

class HospitalOut(HospitalBase):
    hospital_id: str

class StaffBase(BaseModel):
    name: str
    dob: date
    address: str
    phone: str
    staff_role: str
    gender: str
    blood_group: str

    class Config:
        orm_mode = True

class StaffOut(StaffBase):
    staff_id: str


class StaffIn(StaffBase):
    password: str


class Patient(BaseModel):
    patient_id: int
    name: str
    dob: str
    address: str
    phone: str

class Repository(BaseModel):
    blood_id: int
    blood_group: str
    plasma: int
    platelets: int
    rbc: int

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr