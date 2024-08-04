from fastapi import FastAPI
from routes.user import user_route
from routes.balance import balance_route
from routes.prompt import prompt_route
from database.database import init_db
import uvicorn

app = FastAPI()
app.include_router(user_route, prefix='/user')
app.include_router(balance_route, prefix='/balance')
app.include_router(prompt_route, prefix='/prompt')

@app.on_event("startup") 
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)