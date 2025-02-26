from flask import Blueprint
from simpleapi.views.user import login_required
from simpleapi.util.self_parser import use_kwargs
from marshmallow import fields
from simpleapi.models.permission_controller import PermissionModel, UsersPermissionsModel
from simpleapi import db
from simpleapi.util.response_utils import JsonResponse
from simpleapi.util.auth import permission_required
from simpleapi.util.paginator import Paginator
from simpleapi.validate.permission_controller import PermissionSchema
from datetime import datetime as dt

permission_controller_router = Blueprint("permission_controller", __name__)


# 创建和编辑权限
@permission_controller_router.route("/admin/permissions", methods=["POST"])
@login_required
@use_kwargs({
    "name": fields.Str(required=True),
    "code": fields.Str(required=True),
    "id": fields.Int()
})
def create_permission(**kwargs):
    code = kwargs.get('code')
    name = kwargs.get('name')
    id = kwargs.get('id')

    if id:
        db.session.query(PermissionModel).filter_by(id=id).update({"name": name, "code": code})
        db.session.commit()
        return JsonResponse.success({}, "200", "更新成功")
    else:
        obj = db.session.query(PermissionModel).filter_by(code=code).first()
        if obj:
            return JsonResponse.error("权限标识已存在")

        db.session.add(PermissionModel(name=name, code=code))
        db.session.commit()
        return JsonResponse.success({}, "400", "创建成功")


# 删除权限
@permission_controller_router.route("/admin/permissions", methods=["DELETE"])
@login_required
@use_kwargs({
    "id": fields.Int()
})
def del_permission(**kwargs):
    id = kwargs.get('id')

    db.session.query(PermissionModel).filter_by(id=id).delete()
    db.session.commit()
    return JsonResponse.success({}, "200", "删除成功")


def now_ts():
    return int(dt.now().timestamp())


def ts2str(
        cls, t, format_str: str = "%Y-%m-%d %H:%M:%S", acc: str = "s"
) -> str:
    if acc == "s":
        return dt.fromtimestamp(t).strftime(format_str)
    elif acc == "ms":
        return dt.fromtimestamp(t / 1000).strftime(format_str)


# 获取权限列表
@permission_controller_router.route("/admin/permissions", methods=["GET"])
@login_required
@use_kwargs({
    "page": fields.Int(),
    "page_size": fields.Int()
})
def permission_list(**kwargs):
    page = kwargs.get('page')
    page_size = kwargs.get('page_size')
    query = db.session.query(PermissionModel)
    paged = Paginator(query).paginate(page, page_size)

    ret = {
        "total": query.count(),
        "page": paged.page,
        "limit": paged.limit,
        "items": PermissionSchema().dump(paged.items, many=True)
    }

    return JsonResponse.success(ret)


# 给用户绑定功能权限
@permission_controller_router.route("/admin/set-permissions", methods=["POST"])
@login_required
@use_kwargs({
    "user_id": fields.Int(required=True),
    "permission_id": fields.Int(required=True)
})
def set_user_permission(**kwargs):
    user_id = kwargs.get('user_id')
    permission_id = kwargs.get('permission_id')

    obj = db.session.query(UsersPermissionsModel).filter_by(user_id=user_id, permission_id=permission_id).first()
    if obj:
        return JsonResponse.error("用户已有该权限")
    db.session.add(UsersPermissionsModel(user_id=user_id, permission_id=permission_id))
    db.session.commit()
    return JsonResponse.success({}, "200", "设置成功")

