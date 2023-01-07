import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db

router = APIRouter(
    prefix="/donation",
    tags=['Donations'])


@router.get('/', response_model=list[schemas.DonationOut])
def get_donations(db: Session = Depends(get_db)):
    db_donations = db.query(models.Donation).all()
    return db_donations

@router.get('/{donation_id}', response_model=schemas.DonationOut)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    db_donation = db.query(models.Donation).filter(models.Donation.donation_id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"donation with ID {donation_id} not found")
    return db_donation

