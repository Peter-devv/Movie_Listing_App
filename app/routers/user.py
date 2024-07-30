from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, utils, models, database
from ..logger import get_logger

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

logger = get_logger(__name__)

@router.post("/", response_model=schemas.UserResponseModel, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    logger.info("Registering user...")
    hashed_password = utils.hash_password(user_in.password)
    user_in.password = hashed_password
    user = models.User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User with the email: {user.email} registered successfully.")
    return user

@router.get("/{id}", response_model=schemas.UserResponseModel, status_code = status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(detail="User with id: {id} not found", status_code=status.HTTP_404_NOT_FOUND) 
    return user