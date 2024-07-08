@dataclass
class User:
    id: int
    name: str
    password_hash: str
    balance: float
    is_admin: bool