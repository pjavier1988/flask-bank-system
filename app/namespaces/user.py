# app/api/namespaces/user.py
from flask_restx import Namespace, Resource
from app.database import db
from app.models.schemas import UserSchema

user_ns = Namespace('users', description='User operations')

@user_ns.route('/')
class UserList(Resource):
    def get(self):
        pass

    def post(self):
        pass

