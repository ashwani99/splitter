from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func

from datetime import datetime


class SurrogatePK(object):
    id = db.Column(db.Integer, primary_key=True)


class TimeStampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=func.now())


class User(SurrogatePK, TimeStampMixin, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(254), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User({}, id={})>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Bill(SurrogatePK, TimeStampMixin, db.Model):
    __tablename__ = 'bills'

    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    amount = db.Column(db.Float, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id])
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payer = db.relationship('User', foreign_keys=[payer_id])
    paid = db.Column(db.Boolean, default=False) # sqlite doesn't allow server_default=False

    def __init__(self, title, description, author, payer, amount=0):
        db.Model.__init__(
            self, 
            title=title, 
            description=description,
            author=author,
            payer=payer,
            amount=amount)

    def __repr__(self):
        return '<Bill({}, id={})>'.format(self.title, self.id)


class BillSplit(db.Model):
    __tablename__ = 'bill_splits'
    
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False,
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
        primary_key=True)

    user = db.relationship('User', backref=backref('splits'))
    bill = db.relationship('Bill', backref=backref('splits'))

    def __repr__(self):
        return '<BillSplit(bill={}, user={})>'.format(self.bill_id, self.user_id)