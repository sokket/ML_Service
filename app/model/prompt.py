from datetime import datetime as dt

# это сущность для транзакций
@dataclass
class Prompt:
    id: int
    user_id: int
    text: str
    entered_at: dt