from datetime import datetime as dt
from model.app_error import AppError


class Answer:
    id: int
    prompt_id: int
    user_id: int
    cost: float
    text: str
    error: AppError
    returned_at: dt

    def __init__(self, prompt_id, user_id):
        self.prompt_id = prompt_id
        self.user_id = user_id
        self.returned_at = dt()
        self.error = None

    def error_str(prompt: Prompt, error_str: str) -> Answer:
        answ = Answer(prompt.id, prompt.user_id)
        answ.error = AppError(error_str)
        return answ

    def success(prompt: Prompt, text: str) -> Answer:
        answ = Answer(prompt.id, prompt.user_id)
        answ.text = text
        return answ