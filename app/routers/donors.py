import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db
from datetime import date

router = APIRouter(
    prefix="/donors",
    tags=['Donors'])

@router.get('/', response_model=list[schemas.Donor])
def get_donors(locality:str = '',blood_group: str = '',db: Session = Depends(get_db)):
    if locality == '' and blood_group == '':
        db_donors = db.query(models.Donor).all()
    elif locality == '':
        address = locality + ', Mysuru'
        db_donors = db.query(models.Donor).filter(models.Donor.address == address).all()
    elif blood_group == '':
        db_donors = db.query(models.Donor).filter(models.Donor.blood_group == blood_group).all()
    else:
        address = locality + ', Mysuru'
        db_donors = db.query(models.Donor).filter(models.Donor.address == address, models.Donor.blood_group == blood_group).all()
    
    return db_donors


@router.get('/addresses', response_model=list[str])
def get_donors_addresses(db: Session = Depends(get_db)):
    addresses = ['Yelwala','Rupanagar','Devraj Mohalla','Tilaknagar','Jayalakshmipuram','Mandi Mohalla','Kuvempunagar','TK Layout','Udaygiri']

    return addresses

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_donor(request: schemas.DonorBase, db: Session = Depends(get_db)):
    print(request.dob)
    db_donor = db.query(models.Donor).filter(models.Donor.name == request.name).first()
    
    if db_donor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donor with name {request.name} already exists")

    donor_id = 'D0001'
    db_donor = db.query(models.Donor).order_by(models.Donor.donor_id.desc()).first()
    if db_donor:
        donor_id = 'D' + str(int(db_donor.donor_id[1:]) + 1).zfill(4)
    
    dob = request.dob.split('/')
    
    new_donor = models.Donor(
    donor_id=donor_id, 
    name=request.name, 
    address = request.address,
    phone = request.phone,
    dob = date(int(dob[2]),int(dob[1]),int(dob[0])),
    gender = request.gender,
    blood_group = request.blood_group)

    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return Response(status_code=status.HTTP_201_CREATED)