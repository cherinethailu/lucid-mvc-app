from fastapi import FastAPI
from .controllers import auth_controller, post_controller

app = FastAPI()

app.include_router(auth_controller.router)
app.include_router(post_controller.router)

@app.get("/")
def home():
    return {"message": "Lucid FastAPI MVC App is Running!"}
