from app.database import db
from datetime import datetime
from sqlalchemy import CheckConstraint


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        CheckConstraint(type.in_(['deposit', 'withdrawal', 'transfer']), name='check_transaction_type'),
    )
