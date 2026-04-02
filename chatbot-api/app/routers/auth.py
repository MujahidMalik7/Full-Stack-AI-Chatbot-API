from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas
from ..dependencies import get_db, get_current_user
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix = '/auth', tags = ['auth'])

@router.post("/signup", response_model = schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)): 
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    process_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": process_token, "token_type": "bearer"}