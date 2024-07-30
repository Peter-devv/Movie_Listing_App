from typing import List, Optional
from fastapi import Response, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, oauth2, models
from ..logger import get_logger

router = APIRouter(tags=["Movies"], prefix="/movies")
logger = get_logger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MovieResponseModel)
def create_movie(movie_in: schemas.MovieCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    movie = models.Movie(user_id = current_user.id, **movie_in.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    logger.info(f"Movie created successfully...")
    return movie

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.MovieResponseModel])
def get_movies(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    logger.info("Getting movies...")
    movies = db.query(models.Movie).filter(models.Movie.genre.contains(search)).limit(limit).offset(skip).all() 
    logger.info("Movies retrieved successfully.")
    return movies

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieResponseModel)
def get_movie(movie_id: int, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    logger.info(f"{movie.title} gotten successfully.")
    return movie

@router.put("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieResponseModel)
def update_movie(movie_id: int, movie_in: schemas.MovieUpdate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    movie_query =  db.query(models.Movie).filter(models.Movie.id == movie_id)
    movie = movie_query.first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    if movie.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    movie_query.update(movie_in.model_dump(), synchronize_session=False)
    db.commit()
    logger.info("Movie updated successfully.")
    return movie
    
@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    movie_query = db.query(models.Movie).filter(models.Movie.id == movie_id)
    movie = movie_query.first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    
    if movie.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    movie_query.delete(synchronize_session=False)
    db.commit()
    logger.info("Movie deleted successfully.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)