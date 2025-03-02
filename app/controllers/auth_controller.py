from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserSignupSchema, UserLoginSchema
from ..models.user import User
from ..services.auth_service import create_token
from ..dependencies import get_db

# Create an API router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(user_data: UserSignupSchema, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint allows a user to sign up by providing an email and password.
    If the email is already registered, an error is returned.

    Parameters:
        - user_data: UserSignupSchema (Contains email and password)
        - db: Database session dependency

    Returns:
        - JSON response containing the generated authentication token
    """
    # Check if a user with the given email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a new user instance
    user = User(email=user_data.email, password=user_data.password)
    db.add(user)
    db.commit()

    # Generate and return an authentication token
    return {"token": create_token(user.id)}


@router.post("/login")
def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide an access token.

    This endpoint verifies user credentials and returns a JWT token if authentication is successful.

    Parameters:
        - user_data: UserLoginSchema (Contains email and password)
        - db: Database session dependency

    Returns:
        - JSON response containing the authentication token

    Raises:
        - 401 Unauthorized if credentials are invalid
    """
    # Verify user credentials
    user = db.query(User).filter(User.email == user_data.email,User.password == user_data.password).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate and return an authentication token
    return {"token": create_token(user.id)}
