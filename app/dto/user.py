from pydantic import BaseModel

class SignupRequest(BaseModel):
    name: str
    password: str

class SigninRequest(BaseModel):
    name: str
    password: str