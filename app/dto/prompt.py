from pydantic import BaseModel

class PromptRequest(BaseModel):
    text: str
    user_id: str