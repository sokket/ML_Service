from sqlmodel import SQLModel, Field 
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.sql.schema import Column

class User(SQLModel, table=True): 
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    password_hash: str
    balance: float
    is_admin: bool