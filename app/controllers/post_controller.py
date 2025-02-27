from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.post_schema import PostCreateSchema
from ..models.post import Post
from ..services.auth_service import verify_token
from ..dependencies import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/addpost")
def add_post(post_data: PostCreateSchema, token: str, db: Session = Depends(get_db)):
    user = verify_token(token)
    post = Post(text=post_data.text, user_id=user.id)
    db.add(post)
    db.commit()
    return {"postID": post.id}

@router.get("/getposts")
def get_posts(token: str, db: Session = Depends(get_db)):
    user = verify_token(token)
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    return posts

@router.delete("/deletepost")
def delete_post(postID: int, token: str, db: Session = Depends(get_db)):
    user = verify_token(token)
    post = db.query(Post).filter(Post.id == postID, Post.user_id == user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}