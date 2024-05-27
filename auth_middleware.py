'''
auth_middleware.py provided by teacher for using JWT tokens to authenticate users.
Modified it to check for the status of a user as either employer or freelancer
'''
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from model.users import User

def token_required(status=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get("jwt")
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.filter_by(_uid=data["_uid"]).first()
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized"
                    }, 401

                # check if status is provided and if user has the required status passed as an argument
                if status and current_user.status not in status:
                    return {
                        "message": "Insufficient permissions. Required status: {}".format(status),
                        "data": None,
                        "error": "Forbidden"
                    }, 403

            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500

            return f(current_user, *args, **kwargs)

        return decorated

    return decorator