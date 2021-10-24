import db
from enum import Enum
from flask_login import UserMixin

class KeyPair(str, Enum):
    KRAKEN = 'kraken',
    CRYPTOCOM = 'cryptocom'

class User(UserMixin):
    
    def __init__(self, id:str, username:str, email:str, profile_picture:str) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.profile_picture = profile_picture

    def initialize(self):
        # let's not duplicate data in the scheme, try to grab the unique-id
        if db.lookup_user(self.id) == []:
            db.add_user(unique_id=self.id, email=self.email, username=self.username, picture=self.profile_picture)
        else:
            db.update_user_lastlogin(self.id)

    def add_keys(self, pair: str, api: str, secret: str):
        db.update_user_keys(self.id, pair, api, secret)

    def get_keys(self):
        return [db.lookup_user_keys(self.id, 'kraken'), db.lookup_user_keys(self.id, 'cryptocom')]

    def decreypt_keys(self, password: str):
        db.update_user_keys

    def __hash__(self) -> int:
        return self.unique_id.__hash__()
