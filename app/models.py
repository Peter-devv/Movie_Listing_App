from sqlalchemy import Column, Integer, String, FLOAT, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False) 

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User") 
    ratings = relationship("Rating", back_populates="movie")
    comments = relationship("Comment", back_populates="movie")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, nullable=False)
    rating = Column(FLOAT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False) 
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key= True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    movie = relationship("Movie", back_populates="comments")
    user = relationship("User")


class Reply(Base):
    __tablename__ = "replies"
    id = Column(Integer, primary_key= True, nullable=False)
    reply = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    comment = relationship("Comment")   