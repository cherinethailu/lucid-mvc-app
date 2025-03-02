from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.post_schema import PostCreateSchema
from ..models.post import Post
from ..services.auth_service import verify_token
from ..dependencies import get_db

# Create an API router for handling post-related endpoints
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/addpost")
def add_post(post_data: PostCreateSchema, token: str, db: Session = Depends(get_db)):
    """
    Create a new post for an authenticated user.

    Parameters:
        - post_data (PostCreateSchema): The data for the new post.
        - token (str): The authentication token of the user.
        - db (Session): The database session.

    Returns:
        - dict: A dictionary containing the newly created post ID.
    """
    user = verify_token(token)  # Verify user authentication using the token
    post = Post(text=post_data.text, user_id=user.id)  # Create a new Post instance
    db.add(post)  # Add the new post to the database
    db.commit()  # Commit changes to save the post
    return {"postID": post.id}  # Return the created post ID


@router.get("/getposts")
def get_posts(token: str, db: Session = Depends(get_db)):
    """
    Retrieve all posts created by an authenticated user.

    Parameters:
        - token (str): The authentication token of the user.
        - db (Session): The database session.

    Returns:
        - list: A list of posts created by the user.
    """
    user = verify_token(token)  # Verify user authentication
    posts = db.query(Post).filter(Post.user_id == user.id).all()  # Fetch user's posts
    return posts  # Return the list of posts


@router.delete("/deletepost")
def delete_post(postID: int, token: str, db: Session = Depends(get_db)):
    """
    Delete a specific post owned by an authenticated user.

    Parameters:
        - postID (int): The ID of the post to delete.
        - token (str): The authentication token of the user.
        - db (Session): The database session.

    Returns:
        - dict: A success message if the post was deleted.

    Raises:
        - HTTPException (404): If the post does not exist or does not belong to the user.
    """
    user = verify_token(token)  # Verify user authentication
    post = db.query(Post).filter(Post.id == postID, Post.user_id == user.id).first()  # Find the post

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)  # Delete the post
    db.commit()  # Commit changes
    return {"message": "Post deleted"}  # Return success message
