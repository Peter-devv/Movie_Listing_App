from fastapi import status
from .. import schemas 

def test_create_user(client):
    user_data = {
        "email": "peterimade6@gmail.com",
        "password": "514500"
    }
    response = client.post("/users", json=user_data)

    new_user = schemas.UserResponseModel(**response.json())

    assert new_user.email == "peterimade6@gmail.com"
    assert response.status_code == status.HTTP_201_CREATED

def test_get_user(client, test_user):
    response = client.get(f"/users/{test_user['id']}")
    new_user = schemas.UserResponseModel(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert new_user.email == "peterimade6@gmail.com"

def test_user_not_found(client):
    response = client.get("/users/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND