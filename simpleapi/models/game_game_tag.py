from sqlalchemy import (
    Column,
    Integer,
)
from simpleapi import db
import time


class GameGameTagModel(db.Model):
    __tablename__ = "game_game_tag"
    __bind_key__ = "gamesdk"

    id = Column(Integer, primary_key=True)
    tag_group_id = Column(Integer,  comment="")
    tag_id = Column(Integer,  comment="")
    game_type = Column(Integer,  comment="")
    game_id = Column(Integer, comment="")
    # created_time = Column(Integer, nullable=False, default=time.time)
    # updated_time = Column(Integer, default=time.time, onupdate=time.time)

    def to_dict(self):
        return {
            "id": self.id,
            "tag_group_id": self.tag_group_id,
            "tag_id": self.tag_id,
            "game_type": self.game_type,
            "game_id": self.game_id,
            # "created_time": self.created_time,
            # "updated_time": self.updated_time,
        }
