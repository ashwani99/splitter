from werkzeug.security import generate_password_hash, check_password_hash
from app import db, jwt
from sqlalchemy.orm import backref

from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User({}, id={})>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@jwt.user_identity_loader
def get_user_id(user):
    return user.id


@jwt.user_loader_callback_loader
def load_user(id):
    return User.query.get(id)


class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(256))
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def add_participant(self, participant, share, is_payer=False):
        bd = BillDetails.query.filter_by(bill=self, user=participant)
        # update if found
        if bd is not None:
            bd.share = share
            bd.is_payer = is_payer
        else:
            self.bill_details.append(
                BillDetails(bill=self, user=participant, share=share, is_payer=is_payer)
            )

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
    is_payer = db.Column(db.Boolean, default=False)
    share = db.Column(db.Float, nullable=False, default=0.0)

    user = db.relationship('User', backref=backref('bill_details', 
        cascade='all, delete-orphan'))
    bill = db.relationship('Bill', backref=backref('bill_details',
        cascade='all, delete-orphan'))

    def __repr__(self):
        return '<BillDetail(bill={}, user={})>'.format(self.bill_id, self.user_id)