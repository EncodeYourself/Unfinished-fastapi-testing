from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db
from templates import Like
import models

from oauth2 import get_current_user


router = APIRouter(prefix='/likes', tags=['likes'])

@router.post('/')
def add_like(like: Like, db: Session = Depends(get_db), 
             user_id: int = Depends(get_current_user)):
    post_likes = db.query(models.Likes).filter(models.Likes.post_id == like.post_id).first()
    
    if post_likes is None:
        new_like = models.Likes(likes = [user_id.id], **like.dict())
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like
    else:
        post_likes.likes.append(user_id.id)
        db.commit()
