from app import db


class User(db.Model): 
    id = db.column(db.Integer, primary_key = True)
    username = db.column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.Strint(128))

    def _repr__(self):
        return f'<User {self.username}>'