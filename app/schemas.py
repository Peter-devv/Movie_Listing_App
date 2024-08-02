from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    email: EmailStr

    class Config: 
        from_attributes = True

class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str 
    class Config: 
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    genre: str
    director: str 
   
class MovieResponseModel(BaseModel):
    id: int 
    title: str
    genre: str
    director: str
    created_at: datetime
    user_id: int 
    user: UserResponseModel

    class Config: 
        from_attributes = True

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class RatingBase(BaseModel):
    movie_id: int
    rating: int

class RatingResponseModel(BaseModel):
    id: int
    rating: float
    movie_id: int
    movie: MovieResponseModel
    user_id: int

    class Config:
        from_attributes = True

class RatingCreate(RatingBase):
    pass


class TokenData(BaseModel):
    id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class CommentBase(BaseModel):
    movie_id: int
    content: str

class CommentResponseModel(BaseModel):
    id: int 
    content: str
    user_id: int
    movie_id: int
    movie: MovieResponseModel
    created_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(CommentBase):
    pass


class Rating(BaseModel):
    id: int
    rating: float
    user_id: int
    class Config:
        from_attributes = True

class MovieRatingResponseModel(BaseModel):
    id: int
    title: str
    genre: str
    director: str
    user_id: int 
    ratings: List[Rating]

    class Config:
        from_attributes = True

class Comment(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        from_attributes = True

class MovieCommentResponseModel(BaseModel):
    id: int 
    title: str
    genre: str
    director: str
    user_id: int 
    comments: List[Comment]

    class Config:
        from_attributes = True

class ReplyCreate(BaseModel):
    comment_id: int
    content: str