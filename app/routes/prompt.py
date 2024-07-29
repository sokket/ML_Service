from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.database import get_session
from service.sell_model_service import SellModelService
from service.user_service import UserService
from model.prompt import Prompt 
from dto.prompt import PromptRequest
from typing import List

prompt_route = APIRouter(tags=["Prompts"])

async def get_prompt_service() -> SellModelService:
    return SellModelService()

async def get_user_service() -> UserService:
    return UserService()

@prompt_route.get("/", response_model=List[Prompt]) 
async def get_prompts(session=Depends(get_session), service=Depends(get_prompt_service)) -> List[Prompt]:
    return service.get_prompts(session)

@prompt_route.get("/{id}", response_model=Prompt) 
async def get_prompt(id: int, session=Depends(get_session), service=Depends(get_prompt_service)) -> Prompt:
    prompt = service.get_prompt(session, id)
    if prompt is None:
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="Prompt with supplied ID does not exist")
    return prompt

@prompt_route.delete("/{id}")
async def delete_prompt(id: int, session=Depends(get_session), service=Depends(get_prompt_service)) -> dict: 
    prompt = service.get_prompt(session, id)
    if prompt is None:
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="Prompt with supplied ID does not exist")
    service.delete_prompt(session, prompt)

@prompt_route.delete("/")
async def delete_all_prompts(session=Depends(get_session), service=Depends(get_prompt_service)) -> dict: 
    events.clear()
    return {"message": "Prompts deleted successfully"}

@prompt_route.post("/run_model")
async def run_model(req: PromptRequest, 
    session=Depends(get_session),
    service=Depends(get_prompt_service),
    user_service=Depends(get_user_service),
) -> dict: 
    user = user_service.get_by_id(session, req.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id not found")
    service.run_model(session, user, req.text)
    return {"message": "Run successfully"}