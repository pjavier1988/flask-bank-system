from . import auth_bp
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from app.containers import Container
from app.models.schemas import TransferSchema
from app.services.transaction_service import TransactionService
from app.exceptions import InsufficientFundsError, AccountNotExistsError, \
SameAccountError, NegativeValueError, SameAccountError
from dependency_injector.wiring import inject, Provide
from flask import request, jsonify, make_response
from flask import current_app

@auth_bp.route("/auth", methods=['POST'])
def get_token():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if(username == "admin"):
        additional_claims = {"roles": "admin"} 
    else:
        additional_claims = {"roles": "user"}  
    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    response = {
            'code': 0,
            'message': '',
            'data': {"access_token":access_token}
        }
    return response, 200





