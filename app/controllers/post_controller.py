from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.post_schema import PostCreateSchema
from ..models.post import Post
from ..services.auth_service import verify_token
from ..dependencies import get_db
from fastapi import Header

# Create an API router for handling post-related endpoints
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/addpost")
def add_post(post_data: PostCreateSchema,authorization: str = Header(...),  # Extract Authorization header
    db: Session = Depends(get_db)
):
    """
    Create a new post for an authenticated user.

    Parameters:
        - post_data (PostCreateSchema): The data for the new post.
        - authorization (str, from header): The authentication token in the "Bearer <token>" format.
        - db (Session): The database session.

    Returns:
        - dict: A dictionary containing the newly created post ID.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token format. Expected 'Bearer <token>'")

    token = authorization.split("Bearer ")[1]  # Extract the actual token
    user = verify_token(token)  # Verify user authentication using the token

    post = Post(text=post_data.text, user_id=user.id)  # Create a new Post instance
    db.add(post)  # Add the new post to the database
    db.commit()  # Commit changes to save the post
    return {"postID": post.id}  # Return the created post ID

@router.get("/getposts")
def get_posts(
    authorization: str = Header(...),  # Extract Authorization header
    db: Session = Depends(get_db)
):
    """
    Retrieve all posts created by an authenticated user.

    Parameters:
        - authorization (str, from header): The authentication token in the "Bearer <token>" format.
        - db (Session): The database session.

    Returns:
        - list: A list of posts created by the user.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token format. Expected 'Bearer <token>'")

    token = authorization.split("Bearer ")[1]  # Extract the actual token
    user = verify_token(token)  # Verify user authentication

    posts = db.query(Post).filter(Post.user_id == user.id).all()  # Fetch user's posts
    return posts  # Return the list of posts


@router.delete("/deletepost/{postID}")
def delete_post(
    postID: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Delete a specific post owned by an authenticated user.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token format. Expected 'Bearer <token>'")

    token = authorization.split("Bearer ")[1]  # Extract the actual token
    user = verify_token(token)  # Verify user authentication

    post = db.query(Post).filter(Post.id == postID, Post.user_id == user.id).first()  # Find the post

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)  # Delete the post
    db.commit()  # Commit changes
    return {"message": "Post deleted"}  # Return success message
