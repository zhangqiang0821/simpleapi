import os
import sys

import pytest

os.environ['simpleapi_cfg'.upper()] = "test"

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def the_app():
    app.config['TESTING'] = True
    with app.app_context() as f:
        yield app
