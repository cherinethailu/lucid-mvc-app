from sqlalchemy.orm import Session
from .database import SessionLocal
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
