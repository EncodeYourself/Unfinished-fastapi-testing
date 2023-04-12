from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.ext.mutable import MutableList
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, func

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable= False, server_default= "True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now()) #

def like_default(context):
    var = len(context.get_current_parameters()['likes'])
    print(var)
    return var
    
class Likes(Base):
    __tablename__ = 'likes'
    
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'),
                     primary_key=True, nullable=False)
    likes = Column(MutableList.as_mutable(ARRAY(Integer)), nullable=True)
    likes_count = Column(Integer, nullable=True, default=like_default, onupdate=like_default)
    
    