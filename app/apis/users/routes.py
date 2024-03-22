from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from werkzeug.security import check_password_hash
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.models.schemas import UserSchema
from app.containers import Container
from app.apis.users import users_bp
from app.exceptions import UserNotExistsError
from sqlalchemy.exc import IntegrityError
from app.utils.decorators import requires_roles

user_schema = UserSchema()





# Create User

@users_bp.route('/user', methods=['POST'])
@jwt_required()
@requires_roles('admin')
@inject
def create_user(user_service: UserService = Provide[Container.user_service]):
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
   
    try:

        new_user = user_service.create_user(data['username'], data['email'], data['names'])
        response = {
                'code': 0,
                'message': 'User created successfully.',
                'data': user_schema.dump(new_user)
            }
        return response, 201
    except IntegrityError as e:
            response = {
                'code': 1,
                'message': "User Exists",
                'data': {}
            }
            return response, 400
    except UserNotExistsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 404


# Get All Users
@users_bp.route('/user', methods=['GET'])
@jwt_required()
@inject
def get_all_users(user_service: UserService = Provide[Container.user_service]):
    users = user_service.find_all_users()
    response = {
            'code': 0,
            'message': '',
            'data': user_schema.dump(users, many=True)
        }
    return response, 200


@users_bp.route('/user/<username>', methods=['GET'])
@jwt_required()
@inject
def get_user(username,user_service: UserService = Provide[Container.user_service]):
    try:
        user = user_service.find_user(username)
        response = {
                'code': 0,
                'message': '',
                'data':user_schema.dump(user)
            }

        return response, 200
    except UserNotExistsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 404


@users_bp.route('/user/<username>', methods=['PUT'])
@jwt_required()
@inject
def update_user_email(username, user_service: UserService = Provide[Container.user_service]):
    data = request.get_json()
    new_email = data.get('email')
    if not new_email:
        return jsonify({"message": "New email is required"}), 400
    user = user_service.update_user(username, new_email)
    try:
        response = {
            'code': 0,
            'message': 'User email successfully updated.',
            'data': user_schema.dump(jsonify(user_schema.dump(user)))
        }

        return response, 200
    
    except UserNotExistsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 404


@users_bp.route('/user/<username>', methods=['DELETE'])
@jwt_required()
@inject
def delete_user(username, user_service: UserService = Provide[Container.user_service]):
    success = user_service.delete_user(username)
    
    try:
        if success:
            response = {
                'code': 0,
                'message': 'User deleted successfully.',
                'data': {}
            }

            return response, 200
    except UserNotExistsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 404
