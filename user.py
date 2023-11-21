from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, userid, username):
        self.id = userid
        self.userid = userid
        self.username = username

    def __repr__(self):
        return self.userid