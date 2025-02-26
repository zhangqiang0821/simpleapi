from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    SmallInteger,
    Date
)
from simpleapi import db
import time


class GameModel(db.Model):
    __tablename__ = "game_group"
    __bind_key__ = "gamesdk"

    game_group_id = Column(Integer, primary_key=True)
    game_group_name = Column(String(10), comment="游戏组名称")
    game_slug = Column(String(10), comment="游戏拼音简写")
    game_category = Column(Integer, comment="")
    game_dev = Column(Integer, comment="")
    game_cp = Column(Integer, comment="")
    rmb2coin_ratio = Column(Float, comment="")
    earning_ratio = Column(Float, comment="")
    app_content_type = Column(SmallInteger, default=1, comment="类型")
    game_abbr = Column(Integer, default='', comment="")
    enable_vip = Column(Integer, default=0, comment="")
    real_ratio = Column(Float, default=0, comment="")

    def to_dict(self):
        return {
            "game_group_id": self.game_group_id,
            "game_group_name": self.game_group_name,
            "game_slug": self.game_slug,
            "game_category": self.game_category,
            "game_dev": self.game_dev,
            "game_cp": self.game_cp,
            "rmb2coin_ratio": self.rmb2coin_ratio,
            "earning_ratio": self.earning_ratio,
            "app_content_type": self.app_content_type,
            "game_abbr": self.game_abbr,
            "enable_vip": self.enable_vip,
            "real_ratio": self.real_ratio,
        }
