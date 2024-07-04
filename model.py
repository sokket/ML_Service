from datetime import datetime as dt

# stored in db
@dataclass
class User:
    id: int
    name: str
    password_hash: str
    balance: float
    is_admin: bool

# stored in db
@dataclass
class Prompt:
    id: int
    user_id: int
    text: str
    entered_at: dt

# stored in db
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

class AppError:
    text: str

    def __init__(self, text):
        self.text = text

# loaded from config / etcd / etc
@dataclass
class PricingStrategy:
    price_per_run: float

class Model:
    def run(self, user_id: int, prompt: str) -> str:
        # LLM context could be loaded from binary file '{user_id}.ctx'
        pass

class SellModelService:
    model: Model
    pricing_strategy: PricingStrategy

    def __init__(self, model, pricing_strategy):
        self.model = model
        self.pricing_strategy = pricing_strategy

    def run_model(self, user: User, prompt: Prompt) -> Answer:
        price_per_run = self.pricing_strategy.price_per_run

        if user.balance < price_per_run:
            return Answer.error_str(prompt, "not enought points on balance")
  
        text = ''
        try:
            text = self.model.run(user.id, prompt.text)
        except Exception as e:
            # todo: log exception
            return Answer.error_str(prompt, "processing error")

        # change balance only on success
        user.balance -= price_per_run
        
        return Answer.success(prompt, text)

class BalanceService:
    def top_up_balance(user: User, amount: float) -> User:
        # save to db
        pass

class UserService:
    def register(name: str, password: str) -> User:
        # generate password hash, save to db
        pass

    def login(name: str, password: str) -> User:
        # check password hash, load from db
        pass