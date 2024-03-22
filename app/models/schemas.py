# app/schemas.py
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.database import db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from marshmallow_sqlalchemy.fields import Nested

class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        sqla_session = db.session
        load_instance = True

    # Define transaction fields here. For simplicity, using auto_field for all:
    amount = auto_field()
    date = auto_field()
    type = auto_field()


class AccountCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        sqla_session = db.session
        load_instance = True
        include_fk = True  # Includes foreign keys

    account_number = auto_field(required=True)
    balance = auto_field(missing=0.0)  # Defaults to 0.0 if not provided
    description = auto_field(missing=None)
    user_id = auto_field(required=True)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True

class AccountListSchema(SQLAlchemyAutoSchema):
    user = Nested(UserSchema)

    class Meta:
        model = Account
        sqla_session = db.session
        load_instance = True

    balance = auto_field()
    description = auto_field()
    user_id = auto_field()
    transactions = fields.Nested(TransactionSchema, many=True, only=("amount", "date", "type"))




class TransferSchema(Schema):
    from_account = fields.Str(required=True, error_messages={"required": "From account ID is required."})
    to_account = fields.Str(required=True, error_messages={"required": "To account ID is required."})
    amount = fields.Float(required=True, error_messages={"required": "Amount is required."})
    
    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than 0.")


class AccountSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)