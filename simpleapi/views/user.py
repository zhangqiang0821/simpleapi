from flask import Blueprint, request, jsonify
from simpleapi.util.self_parser import use_kwargs
from marshmallow import fields
from simpleapi.util.response_utils import JsonResponse
from simpleapi.models.users import UserModel
from simpleapi import db
from datetime import datetime, timedelta
from jwt import PyJWTError, encode, decode
from functools import wraps
from werkzeug.exceptions import (
    BadRequest,
    UnprocessableEntity,
    InternalServerError,
    NotFound,
    TooManyRequests,
)

user_router = Blueprint("user", __name__)

SECRET_KEY = "your-secret-key-123"  # 替换为强随机字符串
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时


# 添加用户
@user_router.route("/user", methods=['POST'])
@use_kwargs({
    "mobile": fields.Int(required=True),
    "user_name": fields.Str(required=True),
    "password": fields.Str(required=True),
})
def add_user(**kwargs):
    # 获取请求参数
    mobile = kwargs.get('mobile')
    user_name = kwargs.get('user_name')
    password = kwargs.get('password')
    # 查询数据库中是否存在该手机号
    obj = db.session.query(UserModel).filter_by(mobile=mobile).first()
    if obj:
        # 如果存在，返回用户已存在的提示
        return JsonResponse.error({"msg": "用户已存在"})

    # 创建新用户对象
    new_user = UserModel(
        mobile=mobile,
        user_name=user_name,
    )
    new_user.set_password(password)  # 加密密码
    db.session.add(new_user)
    db.session.commit()

    return JsonResponse.success({"mes": "用户添加成功"})


@user_router.route("/login", methods=['POST'])
@use_kwargs({
    "mobile": fields.Int(required=True),
    "password": fields.Str(required=True),
})
def login(**kwargs):
    mobile = kwargs.get('mobile')
    password = kwargs.get('password')
    user_obj = authenticate_user(mobile, password)
    if not user_obj:
        return JsonResponse.error({"msg": "手机号或密码错误"})

    # 生成token
    access_token = create_access_token(user_obj)

    return JsonResponse.success({"access_token": access_token, "user_id": user_obj.id, "user_name": user_obj.user_name})


def create_access_token(user_info):
    payload = {
        "sub": str(user_info.id),
        "username": user_info.user_name,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# 校验登录密码是否正确
def authenticate_user(mobile, password):
    # 根据手机号查询用户
    obj = db.session.query(UserModel).filter_by(mobile=mobile).first()
    # 如果用户不存在，返回成功信息
    if not obj:
        return JsonResponse.success({"msg": "用户不存在"})
    if not obj.check_password(password):  # 检查密码是否正确
        return None
    return obj


# 需要认证的接口
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "code": 401,
                "message": "缺少认证令牌"
            }), 401

            # 解析 Bearer Token
        try:
            # 格式校验：Bearer <token>
            if not auth_header.startswith('Bearer '):
                raise ValueError("令牌格式错误")

            token = auth_header.split(" ")[1].strip()
            if not token:
                raise ValueError("无效的令牌")
        except (IndexError, ValueError) as e:
            return jsonify({
                "code": 401,
                "message": str(e)
            }), 401

        # 验证令牌
        try:
            payload = verify_token(token)  # 使用之前实现的验证函数
            request.user = payload  # 将用户信息存入请求上下文
        except PyJWTError as e:
            return jsonify({
                "code": 401,
                "message": f"令牌验证失败: {str(e)}"
            }), 401
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": f"服务器错误: {str(e)}"
            }), 500

        return func(*args, **kwargs)

    return wrapper


# 校验token
def verify_token(token):
    payload = decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]}  # 强制要求字段
    )
    print('payload', payload)
    user_id = payload.get("sub")
    if not user_id:
        return JsonResponse.success({"status_code": 401, "msg": "无效的认证令牌"})

    return {
        "user_id": user_id,
        "username": payload.get("username"),
        "exp": payload["exp"]
    }


# 用户列表
@user_router.route("/user", methods=['GET'])
@login_required
def user():
    query = db.session.query(UserModel).all()
    data = []
    for item in query:
        data.append(item.to_dict())
    return JsonResponse.success(data)


# 错误处理示例
@user_router.errorhandler(Exception)
def handle_unauthorized(error):
    return jsonify({
        "code": 401,
        "message": "身份验证失败"
    }), 401

