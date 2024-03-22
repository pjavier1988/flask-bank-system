from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash
from dependency_injector.wiring import inject, Provide
from app.services.account_service import AccountService
from app.models.schemas import AccountCreateSchema,AccountListSchema
from app.containers import Container
from app.apis.users import users_bp
from sqlalchemy.exc import IntegrityError



@users_bp.route('/account', methods=['POST'])
@jwt_required()
@inject
def create_account(account_service: AccountService = Provide[Container.account_service]):
    schema = AccountCreateSchema()
    try:
        data = schema.load(request.get_json())
        errors = schema.validate(request.get_json())
        if errors:
            return jsonify(errors), 400
        new_account = account_service.create_account(data)
        response = {
             "code": 0,
             "message": "Account created successfully",
             "data":schema.dump(new_account)
        }
        return response, 201
    except IntegrityError as e:
            response = {
                'code': 1,
                'message': "Account Exists",
                'data': {}
            }
            return response, 400

@users_bp.route('/account', methods=['GET'])
@jwt_required()
@inject
def get_all_counts(account_service: AccountService = Provide[Container.account_service]):
    accounts = account_service.find_all_accounts()
    schema = AccountListSchema(many=True)
    response = {
        "code":0,
        "message":"",
        "data":schema.dump(accounts, many=True)
    }
    return response, 200

'''
@users_bp.route('/account/<account_number>', methods=['GET'])
@jwt_required()
@inject
def get_user(account_service: AccountService = Provide[Container.account_service]):
    user = user_service.find_user(username)
    if user:
        return jsonify(user_schema.dump(user)), 200
    return jsonify({"message": "User not found"}), 404
'''


