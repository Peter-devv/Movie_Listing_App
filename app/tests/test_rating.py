import pytest
from fastapi import status

def test_rate_movie(authorized_client, test_movies):
    response = authorized_client.post("/ratings", json= {
        "movie_id": 1,
        "rating": 3
    })
    assert response.status_code == status.HTTP_201_CREATED
    
def test_rate_movie_not_found(authorized_client):
    rating_data = {
        "movie_id": 1444,
        "rating": 3
    }
    response = authorized_client.post("/ratings", json=rating_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Movie with id:{rating_data['movie_id']} not found"

def test_rate_movie_user_exists(authorized_client, test_ratings):
    response = authorized_client.post("/ratings", json= {
        "movie_id": test_ratings[0].movie_id,
        "rating": test_ratings[0].rating
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == "User has already rated this movie"

def test_get_ratings_for_movie(client, test_ratings):
    response = client.get(f"/ratings/{test_ratings[0].movie_id}")
    assert response.status_code == status.HTTP_200_OK
