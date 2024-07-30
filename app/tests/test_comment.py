import pytest
from fastapi import status

def test_comment_movie(authorized_client, test_movies):
    response = authorized_client.post("/comments", json={
        "movie_id": 1,
        "content": "Interesting!"
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_comment_movie_not_found(authorized_client, test_movies):
    comment_data = {
         "movie_id": 1676,
        "content": "Interesting!"
    }
    response = authorized_client.post("/comments", json=comment_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Movie with id:{comment_data['movie_id']} not found"

def test_get_comments(client, test_movies):
    response = client.get(f"/comments/{test_movies[0].id}")
    assert response.status_code == status.HTTP_200_OK