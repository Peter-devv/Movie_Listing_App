from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2
from ..logger import get_logger


logger = get_logger(__name__)
router = APIRouter(tags=['Authentication'])

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    logger.info("Generating authentication token...")
    user = db.query(models.User).filter(user_credentials.username == models.User.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify_hashed_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
   
    logger.info(f"Token generated for {user.email}")
   
    return {"access_token": access_token, "token_type": "bearer"}
