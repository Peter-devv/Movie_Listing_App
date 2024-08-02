from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from .. import database, schemas, models, oauth2
from ..logger import get_logger
from ..crud import CRUDService

router = APIRouter(prefix="/ratings", tags=["Ratings"])
logger = get_logger(__name__)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.RatingResponseModel)
def rate_movie(rating_in: schemas.RatingCreate, current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()):
    movie = crud.get(rating_in.movie_id, models.Movie)
    logger.info("Rating movie...")
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Movie with id:{rating_in.movie_id} not found")
    existing_rating = crud.get_existing_rating(rating_in, models.Rating, current_user)
    if existing_rating:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User has already rated this movie")
    rating = crud.rate_movie(rating_in, models.Rating, current_user) 
    logger.info("Movie rated successfully.")
    return rating

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieRatingResponseModel)
def get_ratings_for_movie(movie_id: int, crud: CRUDService = Depends()):
    movie = crud.get(movie_id, models.Movie)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    new_movie = crud.get_ratings_for_movie(movie_id, models.Movie)
    logger.info(f"Retrieving ratings for {movie.title}")
    if not new_movie:
        logger.error("No ratings found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ratings found")
    logger.info(f"Ratings for movie: {movie.title} retrieved successfully")
    return new_movie
