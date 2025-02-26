from flask import Response
import json


def make_response(msg="successful", *, data=None, code=0, errmsg=None):
    ret = {"code": code, "msg": msg}

    if data is not None:
        ret["data"] = data
    if errmsg is not None:
        ret["errmsg"] = errmsg

    return Response(json.dumps(ret), mimetype="application/json")
