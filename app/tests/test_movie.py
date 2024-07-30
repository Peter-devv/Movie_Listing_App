import pytest
from fastapi import status
from .. import schemas


@pytest.mark.parametrize("title, genre, director", [
    ("The Punisher", "Action thriller", "Marvel Studios"),
    ("The Awakening", "Horror", "AJS Studios"),
    ("Twilight series", "Mystery", "Universal Studios")
])
def test_create_movie(authorized_client, test_user, title, genre, director):
    
    response = authorized_client.post("/movies", json={
        "title": title,
        "genre": genre,
        "director": director
    })

    new_movie = schemas.MovieResponseModel(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert new_movie.title == title
    assert new_movie.genre == genre
    assert new_movie.director == director
    assert new_movie.user_id == test_user['id']

def test_uauthorized_user_create_movie(client):
    response = client.post("/movies", json={"title": "The Punisher", "genre":"Action thriller", "director":"Marvel Studios"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_all_movies(client, test_movies):
    response = client.get("/movies") 
    def validate(movie):
        return schemas.MovieResponseModel(**movie)
    movies_map = map(validate, response.json())
    movies_list = list(movies_map)
    assert len(response.json()) == len(test_movies)
    assert response.status_code == status.HTTP_200_OK 
    assert movies_list[0].id == test_movies[0].id

def test_get_one_movie(client, test_movies):
    response = client.get(f"/movies/{test_movies[0].id}")
    movie = schemas.MovieResponseModel(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert movie.title == test_movies[0].title

def test_get_one_movie_not_exist(client):
    id = 223
    response = client.get(f"/movies/{id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Movie with id:{id} not found"

def test_unauthorized_user_delete_movie(client, test_movies):
    response = client.delete(f"movies/{test_movies[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_movie(authorized_client, test_movies):
     response = authorized_client.delete(f"movies/{test_movies[0].id}")
     assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_movie_non_exist(authorized_client):
    response = authorized_client.delete(f"movies/8000")
    response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_other_user_movie(authorized_client, test_movies):
    response = authorized_client.delete(f"movies/{test_movies[3].id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_movie(authorized_client, test_movies):
    data = {
        "title": "Man of Steel",
        "genre": "Superhero",
        "director": "DC Comics" 
    }
    response = authorized_client.put(f"/movies/{test_movies[0].id}", json=data)

    updated_movie = schemas.MovieResponseModel(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert updated_movie.title == data['title']
    assert updated_movie.genre == data['genre']

def test_update_other_user_movie(authorized_client, test_movies, test_user_two):
    data = {
        "title": "Man of Steel",
        "genre": "Superhero",
        "director": "DC Comics" 
    }
    response = authorized_client.put(f"/movies/{test_movies[3].id}", json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_unauthorized_user_update_movie(client, test_movies):
    response = client.put(f"/movies/{test_movies[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_movie_non_exist(authorized_client):
    response = authorized_client.put(f"/movies/8000")
    response.status_code == status.HTTP_404_NOT_FOUND