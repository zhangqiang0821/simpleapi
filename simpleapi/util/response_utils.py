# coding:utf8
from flask import make_response, jsonify


class JsonResponse:

    @classmethod
    def success(cls, data, status_code=200, msg=""):
        return make_response(jsonify({"data": data, "error": 0, "msg": msg}), status_code)

    @classmethod
    def error(cls, msg='error', status_code=400):
        return make_response(jsonify({"msg": msg, 'error': 1}), status_code)

