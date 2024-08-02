from typing import List, Optional
from fastapi import Response, APIRouter, status, Depends, HTTPException
from .. import schemas, oauth2, models
from ..crud import CRUDService
from ..logger import get_logger

router = APIRouter(tags=["Movies"], prefix="/movies")
logger = get_logger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MovieResponseModel)
def create_movie(movie_in: schemas.MovieCreate, current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()):
    movie = crud.create(movie_in, models.Movie, current_user)
    logger.info(f"Movie created successfully...")
    return movie

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.MovieResponseModel])
def get_movies(limit: int = 10, skip: int = 0, search: Optional[str] = '', crud: CRUDService = Depends()):
    logger.info("Getting movies...")
    movies = crud.get_movie(models.Movie, limit, skip, search)
    logger.info("Movies retrieved successfully.")
    return movies

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieResponseModel)
def get_movie(movie_id: int, crud: CRUDService = Depends()):
    movie = crud.get(movie_id, models.Movie)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    logger.info(f"{movie.title} gotten successfully.")
    return movie

@router.put("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieResponseModel)
def update_movie(movie_id: int, movie_in: schemas.MovieUpdate, current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()):
    movie = crud.get(movie_id, models.Movie)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    if movie.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    crud.update(movie_id, movie_in, models.Movie) 
    logger.info("Movie updated successfully.")
    return movie
    
@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()):
    movie = crud.get(movie_id, models.Movie)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    
    if movie.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    crud.delete(movie_id, models.Movie)
    logger.info("Movie deleted successfully.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)