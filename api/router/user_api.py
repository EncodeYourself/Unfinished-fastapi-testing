from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db
from templates import *
import models
from utils import hash_password
#import models
#%%

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code = status.HTTP_201_CREATED, response_model=UserOut)
def create_user(new_user: NewUser, db: Session = Depends(get_db)):
    
    new_user.password = hash_password(new_user.password)
    
    user = models.User(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/')
def get_user_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{idx}', response_model=UserOut)
def get_user(idx, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == idx).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the id was not found')
    else:
        return user