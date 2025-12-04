class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def to_json(self):
        return{'user_id': self.user_id, 'name': self.name, 'email': self.email}
    