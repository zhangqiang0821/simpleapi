# -*- coding:utf-8 -*-

import uuid
import time

from urllib.parse import urlencode


def test_index(client):
    "首页测试"
    rv = client.get('/')
    assert rv.status_code == 200
