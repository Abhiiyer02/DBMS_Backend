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
    dob: date
    address: str
    phone: str

class Repository(BaseModel):
    blood_id: int
    blood_group: str
    plasma: int
    platelets: int
    rbc: int
    

class RequestBase(BaseModel):
    hospital_id: str
    patient_case: str
    blood_group: str
    blood_component: str
    quantity: int


    class Config:
        orm_mode = True

class Request(RequestBase):
    request_id: str
    status: str

class DonorBase(BaseModel):
    name: str
    gender: str
    dob: str
    blood_group: str
    phone:str
    address: str

    class Config:
        orm_mode = True

class Donor(DonorBase):
    donor_id: str

class BloodComponent(BaseModel):
    packet_id: str
    component_type:str
    blood_id: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr