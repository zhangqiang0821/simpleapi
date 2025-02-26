from flask import Blueprint, request
from simpleapi import db
from simpleapi.models.game import GameModel
from simpleapi.models.game_game_tag import GameGameTagModel
from simpleapi.models.game_tag import GameTagModel
from simpleapi.util.response_utils import JsonResponse
from simpleapi.util.self_parser import use_kwargs
from simpleapi.util.paginator import Paginator
from simpleapi.validate.game import AddGameSchema, GameSchema
from marshmallow import fields
from sqlalchemy import func
from simpleapi.util.auth import permission_required
from simpleapi.views.user import login_required

index_router = Blueprint("game", __name__)


@index_router.route("/game", methods=['POST'])
@permission_required('kfapi_task_manage')
@login_required
@use_kwargs(AddGameSchema, location="json")
def add_game(**kwargs):
    if kwargs.get('id'):
        obj = db.session.query(GameModel).filter(GameModel.game_group_id == kwargs.get('id')).first()
        for col in GameModel.__table__.columns:
            if col.name in request.json:
                setattr(obj, col.name, request.json.get(col.name))

        # 5236
        # 游戏和标签关联表
        conds = [GameGameTagModel.game_id == kwargs.get('id')]
        obj2 = db.session.query(GameGameTagModel).filter(*conds).first()
        obj2.tag_id = kwargs.get('tag_id')
        db.session.commit()

    else:
        new_obj = GameModel(
            game_group_name=kwargs.get('game_group_name'),
            game_slug=kwargs.get('game_slug'),
            game_category=kwargs.get('game_category'),
            game_dev=kwargs.get('game_dev'),
            game_cp=kwargs.get('game_cp'),
            rmb2coin_ratio=kwargs.get('rmb2coin_ratio'),
            earning_ratio=kwargs.get('earning_ratio'),
            game_abbr=kwargs.get('game_abbr'),
        )
        db.session.add(new_obj)
        db.session.flush()

        game_obj = db.session.query(GameTagModel).filter(GameTagModel.id == kwargs.get('tag_id')).first_or_404(
            '标签不存在')
        # 游戏和标签关联表
        db.session.add(GameGameTagModel(
            tag_group_id=game_obj.tag_group_id,
            tag_id=kwargs.get('tag_id'),
            game_type=1,
            game_id=new_obj.game_group_id,  # 新建游戏id
        ))
        db.session.commit()

    return JsonResponse.success({})


@index_router.route("/game", methods=['DELETE'])
@use_kwargs({"id": fields.Int(required=True)})
def del_game(**kwargs):
    db.session.query(GameModel).filter(GameModel.game_group_id == kwargs.get('id')).delete()
    db.session.query(GameGameTagModel).filter(GameGameTagModel.game_id == kwargs.get('id')).delete()
    db.session.commit()
    return JsonResponse.success({})


@index_router.route("/game", methods=['GET'])
@use_kwargs({"tag_id": fields.Int(load_default=None), "page": fields.Int(load_default=1),
             "page_size": fields.Int(load_default=20)})
def game_list(**kwargs):
    page = kwargs.get('page')  # 页码，从1开始
    page_size = kwargs.get('page_size')  # 每页显示的记录数
    tag_id = kwargs.get("tag_id")
    conds = []
    tag_id is not None and conds.append(GameGameTagModel.tag_id == tag_id)

    query = (
        db.session.query(GameModel)
        .outerjoin(GameGameTagModel, GameModel.game_group_id == GameGameTagModel.game_id)
        .outerjoin(GameTagModel, GameGameTagModel.tag_id == GameTagModel.id)
        .filter(*conds)
        .with_entities(
            GameModel.game_group_id,
            GameModel.game_group_name,
            GameModel.game_slug,
            GameModel.game_category,
            GameModel.game_dev,
            GameModel.game_cp,
            GameModel.rmb2coin_ratio,
            GameModel.earning_ratio,
            GameModel.app_content_type,
            GameModel.game_abbr,
            GameModel.enable_vip,
            GameModel.real_ratio,
            GameTagModel.id.label("tag_id"),
            GameTagModel.name.label("tag_name")
        )
    )

    paged = Paginator(query).paginate(page, page_size)

    ret = {
        "total": query.count(),
        "page": paged.page,
        "limit": paged.limit,
        "items": paged.items,
    }
    return JsonResponse.success(ret)
