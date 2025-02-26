from flask import Blueprint, request, jsonify
from simpleapi.util.self_parser import use_kwargs
from marshmallow import fields
from simpleapi.util.response_utils import JsonResponse
from simpleapi.models.game_tag import GameTagModel, GameTagGroupModel
from simpleapi import db
from collections import defaultdict
from simpleapi.views.user import login_required

game_tag_router = Blueprint("game_tag", __name__)


# 而且是有标签组的，进阶你可以尝试联表查询返回个二级嵌套的枚举接口，标签组是game_tag_group表
@game_tag_router.route("/game_tag", methods=['GET'])
@login_required
def game_tag_tree():
    query = (db.session.query(GameTagGroupModel, GameTagModel).outerjoin(GameTagModel, GameTagGroupModel.id == GameTagModel.tag_group_id).order_by(GameTagModel.id))

    group_map = defaultdict(list)

    for group, game in query:

        if game:  # 处理可能为空的游戏
            group_map[group].append(game)
        else:
            group_map[group] = []

    print(group_map.items())
    # 构造嵌套结构
    result = []
    for group, games in group_map.items():
        group_data = {
            "group_id": group.id,
            "group_name": group.name,
            "games": [
                {"game_id": game.id, "game_name": game.name}
                for game in games
            ]
        }
        result.append(group_data)

    print(result)
    return JsonResponse.success(result)
