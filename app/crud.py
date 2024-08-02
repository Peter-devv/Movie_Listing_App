from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from . import database

class CRUDService:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create(self, data_obj, model, current_user):
        model_obj = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(model_obj)
        self.db.commit()
        self.db.refresh(model_obj)
        return model_obj

    def create_user(self, data_obj, model, hashed_password):
        data_obj.password = hashed_password
        model_obj = model(**data_obj.model_dump())
        self.db.add(model_obj)
        self.db.commit()
        self.db.refresh(model_obj)
        return model_obj

    def get_movie(self, model, limit, skip, search):
        movies = self.db.query(model).filter(model.genre.contains(search)).limit(limit).offset(skip).all()
        return movies

    def get(self, id, model):
        model_obj = self.db.query(model).filter(model.id == id).first()
        if not model_obj:
            return None
        return model_obj

    def get_query_by_id(self, id, model):
        query_result = self.db.query(model).filter(model.id == id)
        return query_result

    def update(self, id, data_obj, model):
        query = self.get_query_by_id(id, model)
        query.update(data_obj.model_dump(), synchronize_session=False)
        self.db.commit()

    def delete(self, id, model):
        query = self.get_query_by_id(id, model)
        query.delete(synchronize_session=False)
        self.db.commit()

    def get_user_by_email(self, email, model):
        user = self.db.query(model).filter(model.email == email).first()
        if user:
            return user
        return None

    def get_ratings_for_movie(self, id, model):
        query = self.get_query_by_id(id, model)
        movie = query.options(joinedload(model.ratings)).first()
        if movie:
            return movie
        return None

    def get_existing_rating(self, data_obj, model, current_user):
        existing_rating = self.db.query(model).filter(
            model.movie_id == data_obj.movie_id,
            model.user_id == current_user.id
        ).first()
        if existing_rating:
            return existing_rating
        return None

    def rate_movie(self, data_obj, model, current_user):
        rating = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def comment_movie(self, data_obj, model, current_user):
        comment = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments_for_movie(self, id, model):
        query = self.get_query_by_id(id, model)
        movie = query.options(joinedload(model.comments)).first()
        if movie:
            return movie
        return None

    def reply_comment(self, data_obj, model, current_user):
        reply = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(reply)
        self.db.commit()
        self.db.refresh(reply)
        return reply
    
