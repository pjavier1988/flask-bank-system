from sqlalchemy.orm import relationship
from app.database import db
#from app.models.account import Account
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    names = db.Column(db.String(150), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    #accounts = db.relationship(Account, backref='owner')


