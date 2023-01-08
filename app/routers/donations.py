import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db
from datetime import date

router = APIRouter(
    prefix="/donations",
    tags=['Donations'])


@router.get('/', response_model=list[schemas.Donations])
def get_donations(db: Session = Depends(get_db)):
    db_donations = db.query(models.Donation).all()
    return db_donations


@router.get('/{donation_id}', response_model=schemas.Donations)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    db_donation = db.query(models.Donation).filter(models.Donation.donation_id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"donation with ID {donation_id} not found")
    return db_donation

@router.post('/')
def create_donation(request: schemas.DonationsBase, db: Session = Depends(get_db)):
    donation_id = 'DON0001'

    db_donation = db.query(models.Donation).order_by(models.Donation.donation_id.desc()).first()
    if db_donation:
        donation_id = 'DON' + str(int(db_donation.donation_id[3:]) + 1).zfill(4)
    
    result = True if request.result == 'Positive' else False

    new_donation = models.Donation(
        donation_id=donation_id, 
        donor_id=request.donor_id, 
        staff_id=request.staff_id,
        donation_occasion=request.donation_occasion,
        blood_group=request.blood_group,
        result =result,
        donation_date=date.today())
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    if result:
        blood_in_db = db.query(models.Repository).filter(models.Repository.blood_group == request.blood_group)

        if blood_in_db.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blood group {request.blood_group} not found in repository")

        blood_in_db.update(blood_group = request.blood_group,platelets = models.Repository.platelets + 1, plasma = models.Repository.plasma + 1, rbc = models.Repository.rbc + 1,synchronize_session=False)

        db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

