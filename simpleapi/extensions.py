from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

db = SQLAlchemy()
sentry = Sentry()