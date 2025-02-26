# -*- coding: utf-8 -*-

import importlib

from flask import Flask, request, jsonify

from simpleapi.extensions import db, sentry
from simpleapi.urls import routers
from simpleapi.util.mylog import log_err, log_info


def load_config_class(config_name):
    """导入config配置"""
    config_class_name = "%sConfig" % config_name.capitalize()
    app_name = __name__
    mod = importlib.import_module('%s.config.%s' % (app_name, config_name))
    config_class = getattr(mod, config_class_name, None)
    return config_class

def create_app(config_name):
    """创建app"""
    app = Flask(__name__)
    config_class = load_config_class(config_name)
    app.config.from_object(config_class)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprint(app)
    configure_logger(app)
    configure_sentry(app)
    return app

def configure_sentry(app):
    if app.config.get("SENTRY_ENABLE"):
        sentry.init_app(app)

def configure_logger(app):
    if app.config.get("GUNICORN_LOGGER_ENABLE"):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

def configure_blueprint(app):
    for blueprint, url_prefix in routers:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

def configure_extensions(app):
    db.init_app(app)

def configure_errorhandlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(state=0, code="401", msg=str(error))

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(state=0, code="403", msg=str(error))

    @app.errorhandler(404)
    def page_not_found(error):
        error_msg = error.description \
            if hasattr(error, 'description') else str(error)
        log_info('HTTP_404', error_msg)
        return jsonify(state=0, code="404", msg=error_msg)

    @app.errorhandler(422)
    def error_request_argument(error):
        data = getattr(error, 'data')
        if data:
            # Get validations from the ValidationError object
            messages = data['messages']
        else:
            messages = ['Invalid request']
        log_info('HTTP_422', messages)
        return jsonify(state=0,code="422",msg=messages)

    @app.errorhandler(500)
    def server_error(error):
        log_err('HTTP_500', error)
        return jsonify(state=0, code="500", msg=error.description)
