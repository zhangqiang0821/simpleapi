from marshmallow import Schema, fields


class GameTagSchema(Schema):
    id = fields.Int()
    tag_group_id = fields.Int()
    org_id = fields.Int()
    name = fields.Str()
