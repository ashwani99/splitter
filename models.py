from werkzeug.security import generate_password_hash, check_password_hash
from app import db

from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}, id={}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)