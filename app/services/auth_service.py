import jwt
import datetime
from ..database import SessionLocal
from ..models.user import User
from fastapi import HTTPException, status
from ..config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES


def create_token(user_id: int):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"user_id": user_id, "exp": expiration}, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        db = SessionLocal()
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        db.close()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
