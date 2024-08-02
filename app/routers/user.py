from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, utils, models
from ..logger import get_logger
from ..crud import CRUDService

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

logger = get_logger(__name__)

@router.post("/", response_model=schemas.UserResponseModel, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, crud: CRUDService = Depends()):
    logger.info("Registering user...")
    if crud.get_user_by_email(user_in.email, models.User):
        logger.error(f"{user_in.email} already registered")
        raise HTTPException(detail=f"{user_in.email} already registered", status_code=status.HTTP_404_NOT_FOUND)
    hashed_password = utils.hash_password(user_in.password)
    user = crud.create_user(user_in, models.User, hashed_password)
    logger.info(f"User with the email: {user.email} registered successfully.")
    return user

@router.get("/{id}", response_model=schemas.UserResponseModel, status_code = status.HTTP_200_OK)
def get_user(id: int, crud: CRUDService = Depends()): 
    user = crud.get(id, models.User)
    if not user:
        raise HTTPException(detail="User with id: {id} not found", status_code=status.HTTP_404_NOT_FOUND) 
    return user