from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.oauth2 import create_acces_token
from app.config import settings

TESTING_DATABASE_URL=f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.TEST_DATABASE_NAME}"

engine = create_engine(TESTING_DATABASE_URL)
TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client(session):
    def override_db():
        yield session
        
    app.dependency_overrides[get_db] = override_db
    yield TestClient(app)

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(client):
    user_data = {'email':'email@email.com', 'password':'password'}
    user = client.post('/users/', json=user_data)
    new_user = user.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def acces_token(test_user):
    user_data = {'user_id':test_user['id']}
    token = create_acces_token(user_data)
    return token

@pytest.fixture
def test_articles(test_user, session):
    article_data = [{
        "title": "1title",
        "content": "1 content",
        "owner_id": test_user['id']
    }, {
        "title": "2 title",
        "content": "2 content",
        "owner_id": test_user['id']
    },
        {
        "title": "3 title",
        "content": "3 content",
        "owner_id": test_user['id']
    }, {
        "title": "4 title",
        "content": "4 content",
        "owner_id": test_user['id']
    }]

    def create_article_model(post):
        return models.Articles(**post)

    article_map = map(create_article_model, article_data)
    articles = list(article_map)

    session.add_all(articles)
    session.commit()

    articles = session.query(models.Articles).all()
    return articles



