from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import database, schemas, models, oauth2
from ..logger import get_logger

router = APIRouter(prefix="/ratings", tags=["Ratings"])
logger = get_logger(__name__)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.RatingResponseModel)
def rate_movie(rating_in: schemas.RatingCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == rating_in.movie_id).first()
    logger.info("Rating movie...")
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Movie with id:{rating_in.movie_id} not found")
    existing_rating = db.query(models.Rating).filter(models.Rating.movie_id == rating_in.movie_id, models.Rating.user_id == current_user.id).first()
    if existing_rating:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User has already rated this movie")
    rating = models.Rating(user_id = current_user.id, **rating_in.model_dump())
    db.add(rating)
    db.commit()
    db.refresh(rating)
    logger.info("Movie rated successfully.")
    return rating

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieRatingResponseModel)
def get_ratings_for_movie(movie_id: int, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    
    new_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).options(joinedload(models.Movie.ratings)).first()
    if not new_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ratings found")
    return new_movie