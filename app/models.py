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
    desc = db.Column(db.String(256))
    amount = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    payer = db.relationship('User', backref='paid_bills')

    def __init__(self, title, payer, desc='', amount=0):
        self.title = title
        self.desc = desc
        self.amount = amount
        self.payer = payer
        # adding the payer with 0 share initially, update it later
        # along with the other participants
        self.add_participant(payer)

    def add_participant(self, participant, share=0):
        for bd in self.bill_details:
            if bd.user is participant:
                break
        else:
            bd = None

        # update if found
        if bd is not None:
            bd.share = share
        else:
            bd = BillDetails(bill=self, user=participant, share=share)

    def remove_participant(self, participant):
        bd = BillDetails.query.filter_by(bill=self, user=participant).scalar()
        if bd is not None:
            self.bill_details.remove(bd)

    def __repr__(self):
        return '<Bill({}, id={})>'.format(self.title, self.id)


class BillDetails(db.Model):
    __tablename__ = 'bill_details'
    
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False,
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
        primary_key=True)
    share = db.Column(db.Float, nullable=False, default=0.0)

    user = db.relationship('User', backref=backref('bill_details', 
        cascade='all, delete-orphan'))
    bill = db.relationship('Bill', backref=backref('bill_details',
        cascade='all, delete-orphan'))

    def __repr__(self):
        return '<BillDetail(bill={}, user={}, share={})>'.format(self.bill_id, self.user_id, self.share)