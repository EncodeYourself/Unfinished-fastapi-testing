from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from templates import UserLogin
import models

from oauth2 import create_access_token
from utils import verification
router = APIRouter(tags=['Auth'])

@router.post('/login')
def log_in(cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Something is wrong!')
    
    if not verification(cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Something is wrong!')
        
    token = create_access_token(data={'user_id': user.id})
    
    return {'access token': token, 'token_type': 'bearer'}