from model.user import User

class UserService:
    def register(name: str, password: str) -> User:
        # generate password hash, save to db
        pass

    def login(name: str, password: str) -> User:
        # check password hash, load from db
        pass