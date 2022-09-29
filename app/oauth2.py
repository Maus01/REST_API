from jose import jwt, JWTError
from .config import settings
from datetime import datetime, timedelta
from .config import settings
from . import schemas
from fastapi import HTTPException, status, Depends
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM



def create_acces_token(data: dict):

    token_data = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data['exp'] = expire
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token:str, exception):
   
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise exception
    return token_data

def logged_user(token:str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized", 
    headers={"WWW-Authenticate":"Bearer"})
    verified_token = verify_token(token, exception)
    user = db.query(models.Users).filter(models.Users.id == verified_token.id).first()
    return user