from fastapi import APIRouter, status,Depends, Response, HTTPException
from sqlalchemy.orm import Session

import schemas,models,utils
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get('/{username}',response_model=schemas.User)
def get_user(username: str,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.User,db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Response(status_code=status.HTTP_201_CREATED)
