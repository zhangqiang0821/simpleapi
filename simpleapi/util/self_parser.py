# coding:utf8
from webargs.flaskparser import FlaskParser
from marshmallow import EXCLUDE


class Parser(FlaskParser):
    DEFAULT_UNKNOWN_BY_LOCATION = {
        "json": EXCLUDE,
        "form": None,
        "json_or_form": None,
        "querystring": EXCLUDE,
        "query": EXCLUDE,
        "headers": EXCLUDE,
        "cookies": EXCLUDE,
        "files": EXCLUDE,
    }


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
