
from fastapi import FastAPI, HTTPException, status
import pytest 
from .database import client, session
from jose import jwt, JWTError 
from ..schemas import Token


def test_login(client, test_user):
    user_data = {
        "username": test_user['email'],
        "password": test_user['password']
    }
    response = client.post("/login", data=user_data)
    token = Token(**response.json())
    payload = jwt.decode(token.access_token, "3952014adb8d1cad2167d9fe932e6d738b757932a3df9289c60d43f41ab41059", algorithms=["HS256"])
    id = payload.get("user_id")
    assert response.status_code == status.HTTP_201_CREATED
    assert token.token_type == "bearer"
    assert id == test_user['id']

@pytest.mark.parametrize("email, password, status_code", [
    ("peterimade6@gmail.com", "78769", status.HTTP_403_FORBIDDEN),
    ("peterosas6@gmail.com", "514500", status.HTTP_403_FORBIDDEN),
    ("peterimade6@example.com", "64646", status.HTTP_403_FORBIDDEN),
    (None, "78769", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("peterimade6@gmail.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY)
])

def test_incorrect_login(client, email, password, status_code):
    response = client.post('/login', data={
        "username": email,
        "password": password
    })

    assert response.status_code == status_code 
