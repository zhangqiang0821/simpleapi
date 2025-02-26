from marshmallow import Schema, fields


class PermissionSchema(Schema):
    id = fields.Int()
    code = fields.Str()
    name = fields.Str()
    ctime = fields.Str()
    utime = fields.Str()
