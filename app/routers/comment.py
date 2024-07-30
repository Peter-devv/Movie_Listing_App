from typing import List
from fastapi import Response, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import database, schemas, oauth2, models
from ..logger import get_logger

router = APIRouter(tags=["Comments"], prefix="/comments")
logger = get_logger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponseModel)
def comment_movie(comment_in: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == comment_in.movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{comment_in.movie_id} not found")
    comment = models.Comment(user_id = current_user.id, **comment_in.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieCommentResponseModel)
def get_comments(movie_id: int, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id:{movie_id} not found")
    new_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).options(joinedload(models.Movie.comments)).first()
    if not new_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comments found")
    logger.info(f"Comments for movie: {movie.title} retrieved successfully")
    return new_movie


@router.post("/reply", status_code=status.HTTP_201_CREATED, response_model = schemas.RatingResponseModel)
def reply_comment(reply_in: schemas.ReplyCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)): 
    comment = db.query(models.Comment).filter(models.Comment.id == reply_in.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id:{reply_in.comment_id} not found")
    reply = models.Reply(user_id = current_user.id, **reply_in.model_dump())
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return reply