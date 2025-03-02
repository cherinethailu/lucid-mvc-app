from pydantic import BaseModel, EmailStr, constr

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
