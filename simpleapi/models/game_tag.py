from sqlalchemy import (
    Column,
    Integer,
    String
)
from simpleapi import db


class GameTagModel(db.Model):
    __tablename__ = "game_tag"
    __bind_key__ = "gamesdk"

    id = Column(Integer, primary_key=True)
    tag_group_id = Column(Integer,  comment="")
    org_id = Column(Integer,  comment="")
    name = Column(String,  comment="")

    def to_dict(self):
        return {
            "id": self.id,
            "tag_group_id": self.tag_group_id,
            "org_id": self.org_id,
            "name": self.name,
        }


class GameTagGroupModel(db.Model):
    __tablename__ = "game_tag_group"
    __bind_key__ = "gamesdk"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer,  comment="")
    name = Column(String, comment="")
    select_type = Column(Integer,  comment="")
    game_type = Column(Integer, comment="")

    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id,
            "name": self.name,
            "select_type": self.select_type,
            "game_type": self.game_type,
        }
