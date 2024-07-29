from model.user import User
from utils.config import get_settings
from utils.hash import hash_password, verify_password

class UserService:

    def __init__(self):
        settings = get_settings()
        self.salt = settings.PASSWORD_SALT

    def register(self, session, name: str, password: str, is_admin: bool = False) -> User:
        new_user = User(
            name=name,
            password_hash=hash_password(password, self.salt),
            balance=0.0,
            is_admin=is_admin
        )
        session.add(new_user) 
        session.commit() 
        session.refresh(new_user)
        return new_user

    def login(self, session, name: str, password: str) -> User:
        user = session.query(User).filter(User.name == name).first()
        if not user:
            raise Exception("User not found")
        if not verify_password(user.password_hash, password, self.salt):
            raise Exception("Wrong password")
        return user
    

    def is_exists(self, session, name) -> bool:
        user = session.query(User).filter(User.name == name).first()
        if user is None:
          return False
        return True

    def get_by_id(self, session, id) -> User:
        user = session.query(User).filter(User.id == id).first()
        return user

    def get_all_users(self, session) -> list[User]:
        return session.query(User).all()
