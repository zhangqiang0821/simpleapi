from functools import wraps
from simpleapi.views.user import login_required
from flask import request
from simpleapi.util.response_utils import JsonResponse
from simpleapi.models.permission_controller import UsersPermissionsModel, PermissionModel
from simpleapi import db


def permission_required(code):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            current_user = getattr(request, 'user', None)

            obj = db.session.query(UsersPermissionsModel).filter_by(user_id=current_user.get('user_id')).first()
            if not obj:
                return JsonResponse.error("没有权限")

            query = (
                    db.session.query(UsersPermissionsModel)
                   .outerjoin(PermissionModel, UsersPermissionsModel.permission_id == PermissionModel.id)
                   .with_entities(
                        UsersPermissionsModel.permission_id,
                        PermissionModel.code
                    ).all())
            code_list = []
            for c in query:
                code_list.append(c.code)

            if code not in [i for i in code_list]:
                return JsonResponse.error("没有权限")

            return func(*args, **kwargs)

        return wrapper

    return decorator
