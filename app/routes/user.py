from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from model.user import User
from dto.user import SigninRequest, SignupRequest
from service.user_service import UserService 
from typing import List

user_route = APIRouter(tags=['User'])

async def get_user_service() -> UserService:
    return UserService()

@user_route.post('/signup')
async def signup(req: SignupRequest, session=Depends(get_session), service=Depends(get_user_service)) -> dict:
    if service.is_exists(session, req.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with supplied username exists")
    
    service.register(session, req.name, req.password)
    return {"message": "User successfully registered!"}

@user_route.post('/signin')
async def signin(req: User, session=Depends(get_session), service=Depends(get_user_service)) -> dict:
    try:
        user = service.login(session, req.name, req.password)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Login failed")
    
    return {"message": "User signed in successfully"}

@user_route.get('/get_all_users', response_model=List[User])
async def get_all_users(session=Depends(get_session), service=Depends(get_user_service)) -> list:
    return service.get_all_users(session)