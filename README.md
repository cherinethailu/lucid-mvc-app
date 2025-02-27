# Lucid MVC App API

## Overview

The **Lucid MVC App API** is a simple RESTful API built using FastAPI. It allows users to authenticate and manage posts. This API supports user signup, login, adding posts, retrieving posts, and deleting posts.

## Features

- User authentication (Signup and Login)
- CRUD operations for posts
- Token-based authorization

## Getting Started

### Prerequisites

- Python 3.7 or higher
- FastAPI
- Uvicorn

### Install Requirements by running:
`pip install -r requirements.txt`

#### Replace these values on the `.env` file to match your local(remote) DB creds:

- `DATABASE_URL=mysql+pymysql://debian-sys-maint:<cherinet-mysql-pswd>@localhost/lucid_app`
- `SECRET_KEY=EaPtOOou8x2DeRqmiamPr7tVXCtfgir8`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`


### To run the app:
Run `uvicorn app.main:app --reload` 
