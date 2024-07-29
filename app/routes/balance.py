from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from model.user import User
from dto.balance import TopUpRequest
from service.balance_service import BalanceService 
from service.user_service import UserService 
from typing import List

balance_route = APIRouter(tags=['Balance'])

async def get_user_service() -> UserService:
    return UserService()

@balance_route.post('/top_up')
async def top_up(
    req: TopUpRequest, 
    session=Depends(get_session), 
    user_service=Depends(get_user_service),
) -> dict:
    user = user_service.get_by_id(session, req.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id not found")
    BalanceService.top_up_balance(session, user, req.amount)
    return {"message": "Balance top up success"}

