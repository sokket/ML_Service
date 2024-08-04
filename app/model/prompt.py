from datetime import datetime as dt
from sqlmodel import SQLModel, Field 
from typing import Optional, List
from datetime import datetime as dt

class Prompt(SQLModel, table=True): 
    id: int = Field(default=None, primary_key=True)
    user_id: int
    text: str
    asked_at: dt
    cost: float
    answer: Optional[str] # async
    error: Optional[str]
    answered_at: Optional[dt]

    def __init__(self, user_id, text):
        self.cost = 0
        self.asked_at = dt.now()
        self.user_id = user_id
        self.text = text
        self.answer = ''