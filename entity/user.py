from flask_login import UserMixin
from entity.user_role import UserRole

approved_writers = ['robin-leach']

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.user_id = user_id

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_role(self):
        return UserRole.Writer if self.user_id in approved_writers else UserRole.Reader
