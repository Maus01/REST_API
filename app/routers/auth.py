from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import utils, models, oauth2, schemas

router = APIRouter(prefix="/login", tags=["Login"])

@router.post('/', response_model=schemas.Token)
def login(user_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_data.username).first()

    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong password or username')

    if not user:
        raise exception

    if not utils.verify(user.password,user_data.password):
        raise exception

    access_token = oauth2.create_acces_token(data = {'user_id':user.id})
    return {'acces_token':access_token,'token_type':'Bearer'}
