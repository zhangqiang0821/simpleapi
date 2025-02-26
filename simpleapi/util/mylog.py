import socket

import simplejson as json
from flask import request, current_app


def log_err(err_type, msg):
    current_app.logger.error(
        json.dumps({
            'host': socket.gethostname(),
            'level': 'ERROR',
            'type': err_type,
            'msg': str(msg),
            "svc": "user-srv",
            "uri": request.path,
            "method": request.method,
            "cntType": request.headers.get("Content-Type", ""),
            "data": request.get_data(),
        }),
        exc_info=True
    )

def log_info(info_type, msg):
    current_app.logger.info(json.dumps({
        'host': socket.gethostname(),
        'level': 'INFO',
        'type': info_type,
        'msg': str(msg),
        "svc": "user-srv",
        "uri": request.path,
        "method": request.method,
        "cntType": request.headers.get("Content-Type", ""),
        "data": request.get_data(),
    }))
