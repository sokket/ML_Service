from model.user import User

class BalanceService:
    def top_up_balance(session, user: User, amount: float) -> User:
        user.balance += amount
        session.add(user) 
        session.commit() 
        session.refresh(user)