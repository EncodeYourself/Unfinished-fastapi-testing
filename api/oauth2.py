from jose import JWTError, jwt
from datetime import datetime, timedelta
from templates import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    raw = data.copy()
    
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    raw.update({'expiration': expiration.isoformat()})
    
    encoded_jwt = jwt.encode(raw, SECRET_KEY, algorithm=[ALGORITHM])
    
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        id: str = payload.get('user_id')
        
        if id is None:
            raise credential_exception
            
        token_data = TokenData(id = id)
    except JWTError: 
        raise credential_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail='Could not validate credentials', 
                                         headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token, credential_exception)