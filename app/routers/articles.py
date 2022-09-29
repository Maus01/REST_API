from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, utils, models, oauth2
from typing import Optional, List


router = APIRouter(prefix="/articles", tags=["articles"])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleOut)
def create_article(article: schemas.Article, db: Session=Depends(database.get_db), user: int =Depends(oauth2.logged_user)):
    
    new_article = models.Articles(owner_id = user.id, **article.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_article(id: int, response_model=schemas.ArticleOut, db: Session=Depends(database.get_db), user: int=Depends(oauth2.logged_user)):

    article=  db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id:{id} doesn't exist")

    return article

@router.get('/', response_model=List[schemas.ArticleOut], status_code=status.HTTP_200_OK)
def get_all_articles(db: Session=Depends(database.get_db),user: int=Depends(oauth2.logged_user), search: Optional[str]=""):

    articles = db.query(models.Articles).filter(models.Articles.title.contains(search)).all()
    return articles


@router.put('/{id}', response_model=schemas.ArticleOut)
def update_article(id: int, updated_article: schemas.Article, db: Session=Depends(database.get_db), user: int=Depends(oauth2.logged_user)):
    article_query = db.query(models.Articles).filter(models.Articles.id == id)
    article=article_query.first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id:{id} doesn't exist")

    if article.owner_id is not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized for this operation")

    article_query.update(updated_article.dict(), synchronize_session=False)
    db.commit()

    return article_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session=Depends(database.get_db), user: int=Depends(oauth2.logged_user)):

    article_query = db.query(models.Articles).filter(models.Articles.id == id)
    article = article_query.first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id:{id} doesn't exist")

    if article.owner_id is not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized for this operation")

    article_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    