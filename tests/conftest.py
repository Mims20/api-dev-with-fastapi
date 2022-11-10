from fastapi.testclient import TestClient
import pytest

from app import models
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}" \
                          f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# default scope of fixture is function
@pytest.fixture()
def db_session():
    # drop database then create fresh one for each testing session
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


#  create test user for all testing
@pytest.fixture
def test_user(client):
    user_data = {"email": "email@email.com",
                 "password": "123456"}
    response = client.post("/users/",
                           json=user_data)
    # save response in new_user and append password, later used for login test
    new_user = response.json()
    new_user["password"] = "123456"

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "email2@email.com",
                 "password": "123456"}
    response = client.post("/users/",
                           json=user_data)
    new_user = response.json()
    new_user["password"] = "123456"

    return new_user


# create token for testing
@pytest.fixture
def create_token(client, test_user):
    return create_access_token(data={"user_id": test_user["id"]})


# return an authorized client after getting token
@pytest.fixture
def authorized_client(client, create_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {create_token}"
    }
    return client


@pytest.fixture
def create_dummy_posts(test_user, db_session, test_user2):
    post_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user2["id"]
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    db_session.add_all(posts)
    db_session.commit()
    all_posts = db_session.query(models.Post).all()
    return all_posts
