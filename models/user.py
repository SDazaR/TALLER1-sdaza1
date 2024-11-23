from flask_login import UserMixin

class User (UserMixin):

    def __init__(self, id:str, username:str, password:str, is_admin: bool) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin
        super().__init__()
