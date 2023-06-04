import pytest
from jose import jwt

from app import schemas
from app.config import settings


# def test_home(client):
#     response = client.get("/")
#     assert response.json().get("message") == "Hello World"
# assert response.status_code == 200


def test_create_user(client):
    response = client.post("/users/",
                           json={"email": "email@email.com", "password": "123456"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "email@email.com"
    assert response.status_code == 201


# login and check validity of jwt token
def test_user_login(client, test_user):
    response = client.post("/login",
                           data={"username": test_user["email"], "password": test_user["password"]})
    # unpack response to get access_token for decoding
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@email.com", "123456", 403),
    ("email@email.com", "wrongpassword", 403),
    ("wrongemail@email.com", "wrongpassword", 403),
    (None, "123456", 422),
    ("email@email.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login",
                           data={"username": email,
                                 "password": password})
    assert response.status_code == status_code
