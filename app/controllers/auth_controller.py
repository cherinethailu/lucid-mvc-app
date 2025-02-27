from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserSignupSchema, UserLoginSchema
from ..models.user import User
from ..services.auth_service import create_token
from ..dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user_data: UserSignupSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=user_data.email, password=user_data.password)
    db.add(user)
    db.commit()
    return {"token": create_token(user.id)}

@router.post("/login")
def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email, User.password == user_data.password).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"token": create_token(user.id)}
