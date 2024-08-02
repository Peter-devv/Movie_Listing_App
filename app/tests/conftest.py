import jwt
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from ..main import app
from .. import models, database, schemas, oauth2
from config import settings


DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                        
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
def client(session): 
    def override_get_db(): 
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db 
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "peterimade6@gmail.com",
        "password": "514500"
    }
    response = client.post("/users", json=user_data) 
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user['password'] = user_data['password'] 
    return new_user

@pytest.fixture
def test_user_two(client):
    user_data = {
        "email": "peterosas345@gmail.com",
        "password": "12345"
    }
    response = client.post("/users", json=user_data) 
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user['password'] = user_data['password'] 
    return new_user

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def test_movies(test_user, test_user_two, session):
    movies_data = [
        {
            "title": "Superman",
            "genre": "Thriller",
            "director": "Mr. Banes",
            "user_id": test_user['id']
        },
        {
            "title": "Spiderman",
            "genre": "Thriller",
            "director": "Marvel",
            "user_id": test_user['id']
        },
        {
            "title": "Antman",
            "genre": "Thriller",
            "director": "Marvel",
            "user_id": test_user['id']
        },
        {
            "title": "Bad boys",
            "genre": "Action, Crime",
            "director": "Will Smith2",
            "user_id": test_user_two['id']
        },
        {
            "title": "The Hitman",
            "genre": "Action",
            "director": "Myles Hunt",
            "user_id": test_user_two['id']
        },
        {
            "title": "The Conman",
            "genre": "Thriller",
            "director": "Myles Jack",
            "user_id": test_user_two['id']
        },
    ]

    def create_movie_model(movie):
        return models.Movie(**movie)

    movie_map = map(create_movie_model, movies_data)
    
    movies = list(movie_map)

    session.add_all(movies)

    session.commit()
    movies = session.query(models.Movie).all()
    return movies


@pytest.fixture
def test_ratings(session, test_user, test_user_two, test_movies):
    ratings_data = [
        {
            "movie_id": test_movies[0].id,
            "rating": 5,
            "user_id": test_user['id']
        },
        {
            "movie_id": test_movies[1].id,
            "rating": 3,
            "user_id": test_user['id']
        },
        {
            "movie_id": test_movies[3].id,
            "rating": 4,
            "user_id": test_user['id']
        },
        {
            "movie_id": test_movies[2].id,
            "rating": 3,
            "user_id": test_user_two['id']
        }
    ]

    def create_rating_model(rating):
        return models.Rating(**rating)

    rating_map = map(create_rating_model, ratings_data)
    
    ratings = list(rating_map)

    session.add_all(ratings)

    session.commit()
    ratings = session.query(models.Rating).all()
    return ratings


@pytest.fixture
def test_comments(session, test_user, test_user_two, test_movies):
    comments_data = [
        {
            "movie_id": test_movies[0].id,
            "content": "Very intriguing",
            "user_id": test_user['id']
        },
        {
            "movie_id": test_movies[1].id,
            "content": "Fascinating",
            "user_id": test_user['id']
        },
        {
            "movie_id": test_movies[2].id,
            "content" : "Superb",
            "user_id": test_user_two['id']
        }
    ]

    def create_comment_model(comment):
        return models.Comment(**comment)

    comment_map = map(create_comment_model, comments_data)
    
    comments = list(comment_map)

    session.add_all(comments)

    session.commit()
    comments = session.query(models.Comment).all()
    return comments
