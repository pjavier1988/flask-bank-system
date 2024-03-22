from app.database import db
from sqlalchemy.orm import relationship
from app.models.transaction import Transaction
from app.models.user import User

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref=db.backref('accounts', lazy=True))

    transactions = relationship(Transaction, backref='account', lazy=True)
