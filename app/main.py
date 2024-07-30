from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, auth, movie, rating, comment
from . import models
from .database import engine 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(movie.router)
app.include_router(rating.router)
app.include_router(comment.router)