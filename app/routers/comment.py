from typing import List
from fastapi import Response, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import database, schemas, oauth2, models
from ..logger import get_logger
from ..crud import CRUDService

router = APIRouter(tags=["Comments"], prefix="/comments")
logger = get_logger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponseModel)
def comment_movie(comment_in: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()):
    movie = crud.get(comment_in.movie_id, models.Movie) 
    logger.info("Commenting movie...")
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{comment_in.movie_id} not found")
    comment = crud.comment_movie(comment_in, models.Comment, current_user)
    logger.info("User commented movie successfully.")
    return comment

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieCommentResponseModel)
def get_comments(movie_id: int, db: Session = Depends(database.get_db), crud: CRUDService = Depends()): 
    movie = crud.get(movie_id, models.Movie)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found") 
    new_movie = crud.get_comments_for_movie(movie_id, models.Movie)
    logger.info(f"Retrieving comments for {movie.title}")
    if not new_movie:
        logger.error("No comments found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comments found")
    logger.info(f"Comments for movie: {movie.title} retrieved successfully")
    return new_movie


@router.post("/reply", status_code=status.HTTP_201_CREATED, response_model = schemas.RatingResponseModel)
def reply_comment(reply_in: schemas.ReplyCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user), crud: CRUDService = Depends()): 
    comment = crud.get(reply_in.comment_id, models.Comment)
    logger.info("Replying comment...")
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id:{reply_in.comment_id} not found")
    reply = crud.reply_comment(reply_in, models.Reply, current_user)
    logger.info("Comment replied successfully.")
    return reply