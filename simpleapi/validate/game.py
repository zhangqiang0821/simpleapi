from marshmallow import Schema, fields, validate


class AddGameSchema(Schema):
    id = fields.Int()
    game_group_name = fields.Str(required=True, validate=validate.Length(max=10))
    game_slug = fields.Str(required=True, validate=validate.Length(max=10))
    game_category = fields.Int(required=True)
    game_dev = fields.Int(required=True)
    game_cp = fields.Int(required=True)
    rmb2coin_ratio = fields.Float(required=True)
    earning_ratio = fields.Float(required=True)
    tag_id = fields.Int()


class GameSchema(Schema):
    game_group_id = fields.Int()
    game_group_name = fields.Str()
    game_slug = fields.Str()
    game_category = fields.Int()
    game_dev = fields.Int()
    game_cp = fields.Int()
    rmb2coin_ratio = fields.Int()
    earning_ratio = fields.Float()
    app_content_type = fields.Int()
    enable_vip = fields.Int()
    real_ratio = fields.Float()
