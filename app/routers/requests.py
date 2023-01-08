import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db

router = APIRouter(
    prefix="/requests",
    tags=['Requests'])

@router.get('/blood_rate',response_model=dict())
def get_blood_rate():
    blood_rate = dict()
    blood_rate['platelets'] = 400
    blood_rate['plasma'] = 400
    blood_rate['RBC'] = 1450
    blood_rate['whole_blood'] = 1450
    return blood_rate

@router.get('/repository_initialize', response_model=list[schemas.Repository])
def repository_initialize(db: Session = Depends(get_db)):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_components = ['Platelets', 'Plasma', 'RBC', 'Whole Blood']

    for blood_group in blood_groups:
        new_repository = models.Repository(blood_group=blood_group,plasma=0,platelets=0,rbc=0)

        db.add(new_repository)
        db.commit()
        db.refresh(new_repository)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get('/{hospital_id}', response_model=list[schemas.Request])
def get_requests_by_hospital_id(hospital_id: str, db: Session = Depends(get_db)):
    requests = db.query(models.Request).filter(models.Request.hospital_id == hospital_id).all()
    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Requests not found")
    return requests


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_request(request: schemas.RequestBase, db: Session = Depends(get_db)):
    db_request = db.query(models.Hospital).filter(models.Hospital.hospital_id == request.hospital_id).first()

    if not db_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with ID {request.hospital_id} does not exist")

    request_id = generate_id(request.blood_group, db)

    db_platelets = db.query(models.Repository).filter(models.Repository.blood_group == request.blood_group, models.Repository.blood_component == 'Platelets')
    
    db_plasma = db.query(models.Repository).filter(models.Repository.blood_group == request.blood_group, models.Repository.blood_component == 'Plasma')
        
    db_rbc = db.query(models.Repository).filter(models.Repository.blood_group == request.blood_group, models.Repository.blood_component == 'RBC')
    
    status = 'Success'
    if request.blood_component == 'Platelets' and db_platelets.count() < request.quantity:
            status = 'Pending'
    
    if request.blood_component == 'Plasma' and db_plasma.count() < request.quantity:
            status = 'Pending'

    if request.blood_component == 'RBC' and db_rbc.count() < request.quantity:
            status = 'Pending'
    
    if request.blood_component == 'Whole Blood' and (db_rbc.count() < request.quantity or db_plasma.count() < request.quantity or db_platelets.count() < request.quantity):
            status = 'Pending'
    
    new_request = models.Request(
        request_id=request_id, 
        hospital_id=request.hospital_id,
        patient_case=request.patient_case,
        blood_group=request.blood_group, 
        blood_component=request.blood_component,
        quantity=request.quantity,
        status = status)

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    if status == 'Success':
        if request.blood_component == 'Platelets':
            db_platelets.update(quantity = db_platelets.count() - request.quantity)
        elif request.blood_component == 'Plasma':
            db_plasma.update(quantity = db_plasma.count() - request.quantity)
        elif request.blood_component == 'RBC':
            db_rbc.update(quantity = db_rbc.count() - request.quantity)
        else:
            db_platelets.update(quantity = db_platelets.count() - request.quantity)
            db_plasma.update(quantity = db_plasma.count() - request.quantity)
            db_rbc.update(quantity = db_rbc.count() - request.quantity)

        db.commit()

    return Response(status_code=status.HTTP_201_CREATED)


def generate_id(blood_group: str,db: Session):
    if blood_group == 'A+':
        request_id = 'RAP001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RAP')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RAP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'A-':
        request_id = 'RAN001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RAN')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RAN' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'B+':
        request_id = 'RBP001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RBP')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RBP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'B-':
        request_id = 'RBN001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RBN')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RBN' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'AB+':
        request_id = 'RABP001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RABP')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RABP' + str(int(db_request.request_id[4:]) + 1).zfill(3)
    elif blood_group == 'AB-':
        request_id = 'RABN001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RABN')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RABN' + str(int(db_request.request_id[4:]) + 1).zfill(3)
    elif blood_group == 'O+':
        request_id = 'ROP001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('ROP')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'ROP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    else:
        request_id = 'RON001'
        db_request = db.query(models.Request).filter(models.Request.request_id.startswith('RON')).order_by(models.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RON' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    return request_id

