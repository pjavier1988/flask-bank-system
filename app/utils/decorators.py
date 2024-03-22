from functools import wraps
from app.database import db
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

def requires_roles(*required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()

            user_roles = claims.get('roles', [])
            if isinstance(user_roles, str):
                user_roles = [user_roles]

            if not set(required_roles).intersection(user_roles):
                return jsonify({
                    "code": 1,
                    "message":"Insufficient permissions",
                    "data":{}
                    }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def transactional(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            with db.session.begin_nested():
                result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    return decorated_function
