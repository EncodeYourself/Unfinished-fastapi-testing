from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db
from templates import post_template, response_template
import models
from oauth2 import get_current_user
from utils import hash_password


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/{idx}')
def get_post(idx, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == idx).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the id was not found')
    else:
        return post

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= response_template)
def new_post(post: post_template, db: Session = Depends(get_db), 
             get_current_user: int = Depends(get_current_user()), 
             user_id: int = Depends(get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{idx}')
def delete_post(idx, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == idx)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'the post with such an id was not found, lol!')
    
    post.delete(synchronize_session=False)
    db.commit()
    return {'message': 'the post was succesfully deleted!'}
    
@router.put('/{idx}')
def update(idx: int, post: post_template, db: Session = Depends(get_db)):
    up_post = db.query(models.Post).filter(models.Post.id == idx)
    if up_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'the post with such an id was not found, lol!')
    
    up_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'the post was succesfully updated!'}

