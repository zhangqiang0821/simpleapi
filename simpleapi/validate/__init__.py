import datetime
from collections import namedtuple

from marshmallow.fields import Field


_Time = namedtuple("Time", ("timestamp", "date", "datetime"))

class UnixTime2DatetimeField(Field):
    default_error_messages = {
        'required': '时间戳不能为空',
        'invalid': '时间戳格式错误',
    }

    def __init__(self, *args, **kwargs):
        super(UnixTime2DatetimeField, self)\
            .__init__(*args, **kwargs)

    def _deserialize(self, value, *args, **kwargs):
        if not value:
            self.fail('required')
        try:
            timestamp = int(value)
            _datetime = datetime.datetime.fromtimestamp(timestamp)
            return _Time(
                timestamp=timestamp, 
                date=_datetime.date(), 
                datetime=_datetime,
            )
        except ValueError as _:
            self.fail('invalid')
