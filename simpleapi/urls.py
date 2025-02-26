# -*- coding: utf-8 -*-

from simpleapi.views.index import index_router
from simpleapi.views.game_tag import game_tag_router
from simpleapi.views.user import user_router
from simpleapi.views.permission_controller import permission_controller_router

routers = (
    (game_tag_router, ''),
    (index_router, ''),
    (user_router, ''),
    (permission_controller_router, '')
)
