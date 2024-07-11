from fastapi import FastAPI
from database.database import get_session, init_db, engine
from sqlmodel import Session
from service.user_service import UserService
from service.balance_service import BalanceService
from service.sell_model_service import SellModelService
from service.model_service import ModelService
from model.pricing_strategy import PricingStrategy
from model.prompt import Prompt
import os

init_db()
print('Init db has been success')

with Session(engine) as session:
    user_service = UserService()
    admin_user = user_service.register(session, 'admin', 'admin', is_admin=True)
    print(admin_user)
    BalanceService.top_up_balance(session, admin_user, 1000)
    print(admin_user)
    strategy = PricingStrategy()
    strategy.price_per_run = 100
    sell_service = SellModelService(ModelService(), strategy)
    prompt = sell_service.run_model(session, admin_user, 'Hello world!')
    print(prompt)
    print(admin_user)
    # Список транзакций
    prompts = sell_service.get_user_prompts(session, admin_user)
    print(prompts)
    try:
        user_service.login(session, 'admin', 'wrong_password')
    except Exception:
        print('Не верный пароль')

    a = user_service.login(session, 'admin', 'admin')
    print(a)

app = FastAPI()


@app.get("/envs")
async def envs():
    return {"envs": os.environ}