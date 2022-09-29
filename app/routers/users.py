from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, utils, models, oauth2

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserPublic)
def create_user(user: schemas.NewUser, db: Session=Depends(database.get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put('/', status_code=status.HTTP_200_OK, response_model=schemas.UserPublic)
def change_password(password_data: schemas.ChangePassword, db: Session=Depends(database.get_db), user: int=Depends(oauth2.logged_user)):

    if not utils.verify(user.password, password_data.old_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')

    user_query = db.query(models.Users).filter(models.Users.email == user.email)


    updated_user = schemas.NewUser(email = user.email, password=utils.hash_password(password_data.new_password))
    print(updated_user)
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()


    return user_query.first()




